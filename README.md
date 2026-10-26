# Python Projekte

<p align="center">
  <strong>Python · discord.py · SQLite</strong><br>
  Ein Discord-Bot mit Moderation, Rollenverwaltung und Levelsystem.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/discord.py-2.7.1-5865F2?logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
</p>

---

## Über das Projekt

Dieses Repository enthält einen Discord-Bot auf Basis von `discord.py`, entstanden im Rahmen des Python-Kurses BACKEND 03 der Developer Akademie.

Das Projekt verbindet die Arbeit mit einer externen API, asynchrone Programmierung, persistente Datenspeicherung und die Entwicklung eigener Bot-Befehle.

## Funktionen

| Bereich              | Funktionen                                                                             |
| -------------------- | -------------------------------------------------------------------------------------- |
| **Moderation**       | Warnungen, Kick, Ban, Timeout und Nachrichten löschen                                  |
| **AutoMod**          | Erkennung von Spam, Links und übermäßiger Großschreibung                               |
| **Verwarnungen**     | Speicherung von Warnungen und automatischer Timeout ab einer konfigurierbaren Schwelle |
| **Levelsystem**      | XP sammeln, Level aufsteigen, Rang anzeigen und Bestenliste abrufen                    |
| **Rollenverwaltung** | Rollen manuell, über Level oder durch Reaktionen vergeben                              |
| **Community**        | Begrüßungsnachrichten und benutzerdefinierte Befehle                                   |
| **Datenbank**        | Speicherung von Leveln, Warnungen, Rollen und Einstellungen in SQLite                  |

## Technologien

- **Python** – Programmiersprache
- **discord.py** – Anbindung an die Discord API
- **SQLite** – lokale Datenbank ohne separaten Datenbankserver
- **python-dotenv** – Laden der Konfiguration aus einer `.env`-Datei
- **Git und GitHub** – Versionsverwaltung und Dokumentation

## Voraussetzungen

- Eine installierte Python-Version, die mit den Abhängigkeiten in `requirements.txt` kompatibel ist
- Ein eingerichteter Discord-Bot
- Die erforderlichen Bot-Berechtigungen für Moderation und Rollenverwaltung

Für die verwendeten Funktionen müssen im Discord Developer Portal die benötigten Gateway Intents aktiviert sein, insbesondere **Message Content Intent** und **Server Members Intent**.

## Installation

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
python -m pip install -r requirements.txt
```

### 4. Umgebungsvariablen konfigurieren

Erstelle im Projektverzeichnis eine Datei namens `.env` und trage dein Discord-Bot-Token ein:

```env
DISCORD_TOKEN=dein_discord_bot_token
```

Ersetze den Platzhalter durch dein tatsächliches Token. Gib dieses niemals weiter und veröffentliche es nicht auf GitHub.

### 5. Bot starten

```powershell
python bot.py
```

Beim Start legt der Bot die benötigten SQLite-Tabellen in der lokalen Datenbank `bot_data.db` an.

## Projektstruktur

```text
python-projekte/
├── utils/
│   └── hallo.py
├── bot.py
├── check_db.py
├── main.py
├── set_level.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Zusätzliche Skripte

- `check_db.py` – zeigt vorhandene Datenbanktabellen und ausgewählte Datensätze an.
- `set_level.py` – setzt das Level eines Benutzers. Vor der Ausführung müssen `USER_ID` und `LEVEL` im Skript geprüft und angepasst werden.
- `main.py` – separates Python-Übungsprogramm.
- `utils/hallo.py` – enthält eine wiederverwendbare Begrüßungsfunktion.

Die Dateien `.env`, `.venv/`, `__pycache__/` und `bot_data.db` werden durch `.gitignore` von der Versionsverwaltung ausgeschlossen.

## Lernziele

- Python strukturiert einsetzen
- Mit einer externen API kommunizieren
- Events und asynchrone Funktionen verwenden
- Daten mit SQLite dauerhaft speichern
- Eigene Befehle und Berechtigungsprüfungen implementieren
- Konfiguration und vertrauliche Zugangsdaten getrennt verwalten
- Änderungen mit Git nachvollziehbar dokumentieren

---

<p align="center">
  <sub>Python-Lernprojekt · Developer Akademie</sub>
</p>
