# Python Projekte

<p align="center">
  <strong>Python · Discord.py · SQLite</strong><br>
  Ein Discord-Bot mit Moderations-, Rollen- und Levelsystem.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.15%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/discord.py-2.7.1-5865F2?logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Status-Learning%20Project-orange" alt="Learning project">
</p>

---

## Über das Projekt

Dieses Repository dokumentiert meine Arbeit mit Python im Rahmen der Weiterbildung bei der Developer Akademie. Im Mittelpunkt steht ein Discord-Bot, an dem ich den Umgang mit APIs, Datenbanken, Events und asynchroner Programmierung praktisch umsetze.

## Funktionen

| Bereich         | Funktion                                                      |
| --------------- | ------------------------------------------------------------- |
| **Moderation**  | Warnungen, Kick, Ban, Timeout und Nachrichten löschen         |
| **AutoMod**     | Erkennung von Spam, Links und übermäßiger Großschreibung      |
| **Levelsystem** | XP sammeln, Level aufsteigen und Rangliste anzeigen           |
| **Rollen**      | Rollen manuell, über Level oder per Reaction vergeben         |
| **Community**   | Begrüßungsnachrichten und eigene Bot-Befehle                  |
| **Persistenz**  | Speicherung von Leveln, Warnungen und Einstellungen in SQLite |

## Tech Stack

- **Python** – Programmiersprache
- **discord.py** – Discord API und Bot-Framework
- **SQLite** – lokale Datenhaltung
- **python-dotenv** – Konfiguration über Umgebungsvariablen

## Projekt starten

### 1. Repository klonen

```powershell
git clone https://github.com/CWhymann/python-projekte.git
cd python-projekte
```

### 2. Virtuelle Umgebung erstellen

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Abhängigkeiten installieren

```powershell
pip install -r requirements.txt
```

### 4. Umgebungsvariable setzen

Lege im Projektverzeichnis eine Datei namens `.env` an:

```env
DISCORD_TOKEN=dein_discord_bot_token
```

> **Wichtig:** Die `.env`-Datei enthält vertrauliche Zugangsdaten und gehört nicht ins Repository.

### 5. Bot starten

```powershell
python bot.py
```

## Projektstruktur

```text
python-projekte/
├── utils/              # Wiederverwendbare Hilfsfunktionen
├── bot.py              # Discord-Bot
├── main.py             # Python-Einstiegspunkt / Übung
├── requirements.txt    # Python-Abhängigkeiten
├── .env                # Lokale Zugangsdaten (nicht versioniert)
├── .gitignore
└── README.md
```

## Lernziele

- Python strukturiert und modular einsetzen
- Mit einer externen API arbeiten
- Daten dauerhaft in SQLite speichern
- Events und asynchrone Funktionen verstehen
- Konfiguration und Secrets sauber verwalten
- Änderungen mit Git versionieren und über GitHub dokumentieren

---

<p align="center">
  <sub>Ein fortlaufendes Lern- und Praxisprojekt.</sub>
</p>
