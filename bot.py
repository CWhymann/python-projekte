import os
import random
import sqlite3
import logging
from collections import deque
from datetime import datetime, timedelta, timezone

import discord
from discord.ext import commands
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- Datenbank ----------
conn = sqlite3.connect("bot_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS levels (
    user_id INTEGER PRIMARY KEY,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    reason TEXT,
    moderator_id INTEGER,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS custom_commands (
    name TEXT PRIMARY KEY,
    response TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS reaction_roles (
    message_id INTEGER,
    emoji TEXT,
    role_id INTEGER,
    PRIMARY KEY (message_id, emoji)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS level_roles (
    level INTEGER PRIMARY KEY,
    role_id INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")

conn.commit()

DEFAULTS = {
    "welcome_channel": "willkommen",
    "warn_threshold": "3",
    "automod_spam": "1",
    "automod_links": "0",
    "automod_caps": "1",
}

BAD_WORDS = ["badword1", "badword2"]  # eigene Liste eintragen
AUTO_TIMEOUT_MINUTES = 10
xp_cooldown = {}
message_times = {}

# ---------- Hilfsfunktionen ----------

def get_setting(key):
    cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
    row = cursor.fetchone()
    return row[0] if row else DEFAULTS[key]


def set_setting(key, value):
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()


def add_xp(user_id, amount):
    cursor.execute("SELECT xp, level FROM levels WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row:
        xp, level = row
        xp += amount
    else:
        xp, level = amount, 0
        cursor.execute("INSERT INTO levels (user_id, xp, level) VALUES (?, ?, ?)", (user_id, xp, level))

    needed = (level + 1) * 100
    leveled_up = False
    while xp >= needed:
        xp -= needed
        level += 1
        leveled_up = True
        needed = (level + 1) * 100

    cursor.execute("UPDATE levels SET xp = ?, level = ? WHERE user_id = ?", (xp, level, user_id))
    conn.commit()
    return leveled_up, level


def add_warning(user_id, reason, moderator_id):
    cursor.execute(
        "INSERT INTO warnings (user_id, reason, moderator_id, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, reason, moderator_id, datetime.now(timezone.utc).isoformat()),
    )
    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM warnings WHERE user_id = ?", (user_id,))
    return cursor.fetchone()[0]


async def punish_if_needed(member, channel, count):
    threshold = int(get_setting("warn_threshold"))
    if count < threshold:
        return
    until = discord.utils.utcnow() + timedelta(minutes=AUTO_TIMEOUT_MINUTES)
    try:
        await member.timeout(until, reason=f"Automatisch nach {count} Verwarnungen")
        await channel.send(
            f"{member.mention} hat {count} Verwarnungen und ist für {AUTO_TIMEOUT_MINUTES} Minuten stummgeschaltet."
        )
    except discord.Forbidden:
        logging.error(f"Keine Berechtigung, {member} zu timeouten.")


async def give_level_roles(member, level):
    cursor.execute("SELECT role_id FROM level_roles WHERE level <= ?", (level,))
    roles = [member.guild.get_role(row[0]) for row in cursor.fetchall()]
    roles = [r for r in roles if r is not None and r not in member.roles]
    if roles:
        try:
            await member.add_roles(*roles, reason="Level-Rolle")
        except discord.Forbidden:
            logging.error("Keine Berechtigung, Level-Rollen zu vergeben.")


def find_violation(message):
    text = message.content
    lower = text.lower()

    if any(word in lower for word in BAD_WORDS):
        return "Beleidigung"

    if get_setting("automod_links") == "1" and any(p in lower for p in ("http://", "https://", "www.")):
        return "Link"

    letters = [c for c in text if c.isalpha()]
    if get_setting("automod_caps") == "1" and len(letters) >= 15:
        if sum(c.isupper() for c in letters) / len(letters) > 0.7:
            return "Großschreibung"

    if get_setting("automod_spam") == "1":
        now = datetime.now(timezone.utc)
        times = message_times.setdefault(message.author.id, deque(maxlen=5))
        times.append(now)
        if len(times) == 5 and now - times[0] < timedelta(seconds=5):
            return "Spam"

    return None

# ---------- Events ----------

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")


@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=get_setting("welcome_channel"))
    if channel:
        await channel.send(f"Willkommen auf dem Server, {member.mention}! 🎉")


@bot.event
async def on_message(message):
    if message.author.bot or message.guild is None:
        return

    if not message.author.guild_permissions.manage_messages:
        reason = find_violation(message)
        if reason:
            try:
                await message.delete()
            except (discord.Forbidden, discord.NotFound):
                pass
            count = add_warning(message.author.id, f"Automod: {reason}", bot.user.id)
            await message.channel.send(
                f"{message.author.mention}, {reason} ist hier nicht erlaubt. Verwarnung Nr. {count}.",
                delete_after=5,
            )
            await punish_if_needed(message.author, message.channel, count)
            return

    now = datetime.now(timezone.utc)
    last = xp_cooldown.get(message.author.id)
    if not last or now - last > timedelta(seconds=60):
        xp_cooldown[message.author.id] = now
        leveled_up, new_level = add_xp(message.author.id, random.randint(5, 15))
        if leveled_up:
            await message.channel.send(f"🎉 {message.author.mention} ist jetzt Level {new_level}!")
            await give_level_roles(message.author, new_level)

    if message.content.startswith("!"):
        parts = message.content[1:].split()
        if parts and bot.get_command(parts[0]) is None:
            cursor.execute("SELECT response FROM custom_commands WHERE name = ?", (parts[0],))
            row = cursor.fetchone()
            if row:
                await message.channel.send(row[0])

    await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member is None or payload.member.bot:
        return
    cursor.execute(
        "SELECT role_id FROM reaction_roles WHERE message_id = ? AND emoji = ?",
        (payload.message_id, str(payload.emoji)),
    )
    row = cursor.fetchone()
    if row:
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(row[0])
        if role:
            await payload.member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    cursor.execute(
        "SELECT role_id FROM reaction_roles WHERE message_id = ? AND emoji = ?",
        (payload.message_id, str(payload.emoji)),
    )
    row = cursor.fetchone()
    if row:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        role = guild.get_role(row[0])
        if member and role:
            await member.remove_roles(role)

# ---------- Basis-Commands ----------

@bot.command()
async def hallo(ctx):
    await ctx.send(f"Hallo {ctx.author.mention}!")


@bot.command()
async def echo(ctx, *, text):
    await ctx.send(text)

# ---------- Rollen ----------

@bot.command()
@commands.has_permissions(manage_roles=True)
async def gib_rolle(ctx, member: discord.Member, *, rollenname: str):
    role = discord.utils.get(ctx.guild.roles, name=rollenname)
    if role is None:
        await ctx.send(f"Rolle '{rollenname}' existiert nicht.")
        return
    await member.add_roles(role)
    await ctx.send(f"{member.mention} hat jetzt die Rolle {rollenname}.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def nimm_rolle(ctx, member: discord.Member, *, rollenname: str):
    role = discord.utils.get(ctx.guild.roles, name=rollenname)
    if role is None:
        await ctx.send(f"Rolle '{rollenname}' existiert nicht.")
        return
    await member.remove_roles(role)
    await ctx.send(f"{member.mention} hat die Rolle {rollenname} verloren.")


@bot.command()
@commands.has_permissions(manage_guild=True)
async def levelrolle(ctx, level: int, role: discord.Role):
    if level < 1:
        await ctx.send("Das Level muss mindestens 1 sein.")
        return
    cursor.execute(
        "INSERT OR REPLACE INTO level_roles (level, role_id) VALUES (?, ?)",
        (level, role.id),
    )
    conn.commit()
    await ctx.send(f"Ab Level {level} bekommt man die Rolle {role.name}.")


@bot.command()
async def levelrollen(ctx):
    cursor.execute("SELECT level, role_id FROM level_roles ORDER BY level")
    rows = cursor.fetchall()
    if not rows:
        await ctx.send("Es sind keine Level-Rollen eingerichtet.")
        return
    lines = []
    for level, role_id in rows:
        role = ctx.guild.get_role(role_id)
        name = role.name if role else f"Unbekannt ({role_id})"
        lines.append(f"Level {level}: {name}")
    await ctx.send("\n".join(lines))

# ---------- Moderation ----------

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Kein Grund angegeben"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} wurde gekickt. Grund: {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Kein Grund angegeben"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} wurde gebannt. Grund: {reason}")


@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, minutes: int, *, reason="Kein Grund angegeben"):
    if minutes < 1 or minutes > 40320:
        await ctx.send("Die Dauer muss zwischen 1 und 40320 Minuten liegen.")
        return
    until = discord.utils.utcnow() + timedelta(minutes=minutes)
    await member.timeout(until, reason=reason)
    await ctx.send(f"{member.mention} ist für {minutes} Minuten stummgeschaltet. Grund: {reason}")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason="Kein Grund angegeben"):
    count = add_warning(member.id, reason, ctx.author.id)
    await ctx.send(f"{member.mention} wurde verwarnt. Grund: {reason} (Verwarnung Nr. {count})")
    await punish_if_needed(member, ctx.channel, count)


@bot.command()
@commands.has_permissions(manage_guild=True)
async def warnschwelle(ctx, anzahl: int):
    if anzahl < 1:
        await ctx.send("Die Schwelle muss mindestens 1 sein.")
        return
    set_setting("warn_threshold", str(anzahl))
    await ctx.send(f"Ab {anzahl} Verwarnungen gibt es automatisch einen Timeout.")


@bot.command()
async def verwarnungen(ctx, member: discord.Member):
    cursor.execute("SELECT reason, timestamp FROM warnings WHERE user_id = ?", (member.id,))
    rows = cursor.fetchall()
    if not rows:
        await ctx.send(f"{member.mention} hat keine Verwarnungen.")
        return
    text = "\n".join(f"- {reason} ({timestamp[:10]})" for reason, timestamp in rows)
    await ctx.send(f"Verwarnungen von {member.mention}:\n{text}")


@bot.command()
@commands.has_permissions(manage_guild=True)
async def automod(ctx, regel: str, status: str):
    regeln = {"spam": "automod_spam", "links": "automod_links", "caps": "automod_caps"}
    if regel not in regeln or status not in ("an", "aus"):
        await ctx.send("Benutzung: !automod <spam|links|caps> <an|aus>")
        return
    set_setting(regeln[regel], "1" if status == "an" else "0")
    await ctx.send(f"Automod '{regel}' ist jetzt {status}.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"{len(deleted) - 1} Nachrichten gelöscht.")
    await msg.delete(delay=3)


@bot.command()
@commands.has_permissions(manage_guild=True)
async def willkommenkanal(ctx, *, kanalname: str):
    set_setting("welcome_channel", kanalname)
    await ctx.send(f"Begrüßungen werden jetzt in '{kanalname}' gepostet.")

# ---------- Leveling ----------

@bot.command()
async def rank(ctx, member: discord.Member = None):
    member = member or ctx.author
    cursor.execute("SELECT xp, level FROM levels WHERE user_id = ?", (member.id,))
    row = cursor.fetchone()
    if not row:
        await ctx.send(f"{member.mention} hat noch keine XP gesammelt.")
        return
    xp, level = row
    await ctx.send(f"{member.mention} ist Level {level} mit {xp} XP.")


@bot.command()
async def leaderboard(ctx):
    cursor.execute("SELECT user_id, xp, level FROM levels ORDER BY level DESC, xp DESC LIMIT 10")
    rows = cursor.fetchall()
    if not rows:
        await ctx.send("Noch keine Daten vorhanden.")
        return
    text = ""
    for i, (user_id, xp, level) in enumerate(rows, start=1):
        user = bot.get_user(user_id)
        name = user.name if user else f"Unbekannt ({user_id})"
        text += f"{i}. {name} – Level {level} ({xp} XP)\n"
    await ctx.send(text)

# ---------- Reaction Roles ----------

@bot.command()
@commands.has_permissions(manage_roles=True)
async def reactionrole(ctx, message_id: int, emoji: str, role: discord.Role):
    try:
        message = await ctx.channel.fetch_message(message_id)
    except discord.NotFound:
        await ctx.send("Nachricht nicht gefunden (muss in diesem Kanal liegen).")
        return
    await message.add_reaction(emoji)
    cursor.execute(
        "INSERT OR REPLACE INTO reaction_roles (message_id, emoji, role_id) VALUES (?, ?, ?)",
        (message_id, emoji, role.id),
    )
    conn.commit()
    await ctx.send(f"Reaction Role eingerichtet: {emoji} → {role.name}")

# ---------- Custom Commands ----------

@bot.command()
@commands.has_permissions(manage_guild=True)
async def addcommand(ctx, name: str, *, response: str):
    cursor.execute("INSERT OR REPLACE INTO custom_commands (name, response) VALUES (?, ?)", (name, response))
    conn.commit()
    await ctx.send(f"Command !{name} wurde hinzugefügt.")


@bot.command()
@commands.has_permissions(manage_guild=True)
async def removecommand(ctx, name: str):
    cursor.execute("DELETE FROM custom_commands WHERE name = ?", (name,))
    conn.commit()
    await ctx.send(f"Command !{name} wurde entfernt.")

# ---------- Fehlerbehandlung ----------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Dir fehlt die Berechtigung für diesen Befehl.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Mir fehlt die Berechtigung dafür (siehe Server-Einstellungen → Rollen).")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Mitglied nicht gefunden. Bitte @mention verwenden (anklicken im Dropdown).")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send("Rolle nicht gefunden.")
    elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
        await ctx.send("Falsche oder fehlende Eingabe. Prüfe die Befehlsbenutzung.")
    elif isinstance(error, commands.CommandInvokeError) and isinstance(error.original, discord.Forbidden):
        await ctx.send("Discord verweigert diese Aktion. Die Rolle des Bots muss höher stehen als die des Ziels.")
    else:
        logging.error(f"Unerwarteter Fehler: {error}")
        await ctx.send("Es ist ein Fehler aufgetreten.")


bot.run(TOKEN)