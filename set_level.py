import sqlite3

USER_ID = 821398245292900433
LEVEL = 100

con = sqlite3.connect("bot_data.db")
con.execute(
    "INSERT INTO levels (user_id, xp, level) VALUES (?, 0, ?) "
    "ON CONFLICT(user_id) DO UPDATE SET xp = 0, level = excluded.level",
    (USER_ID, LEVEL),
)
con.commit()
print(con.execute("SELECT * FROM levels WHERE user_id = ?", (USER_ID,)).fetchone())
con.close()
