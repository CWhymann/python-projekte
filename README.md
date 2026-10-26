# Python Projects

<p align="center">
  <strong>Python · discord.py · SQLite</strong><br>
  A Discord bot with moderation, role management, and a leveling system.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/discord.py-2.7.1-5865F2?logo=discord&logoColor=white" alt="discord.py">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
</p>

---

## About the Project

This repository contains a Discord bot built with `discord.py`, created as part of the Python course **BACKEND 03** at Developer Akademie.

The project covers working with an external API, asynchronous programming, persistent data storage, and building custom bot commands.

## Features

| Area               | Functionality                                                                   |
| ------------------ | -------------------------------------------------------------------------------- |
| **Moderation**      | Warnings, kick, ban, timeout, and message deletion                              |
| **AutoMod**         | Detection of spam, links, and excessive capitalization                         |
| **Warnings**        | Warning storage with automatic timeout above a configurable threshold          |
| **Leveling**        | Earn XP, level up, view rank, and check the leaderboard                        |
| **Role Management** | Assign roles manually, by level, or via reactions                              |
| **Community**       | Welcome messages and custom commands                                            |
| **Database**        | Levels, warnings, roles, and settings stored in SQLite                         |

## Technologies

- **Python** – programming language
- **discord.py** – Discord API integration
- **SQLite** – local database, no separate database server required
- **python-dotenv** – loads configuration from a `.env` file
- **Git & GitHub** – version control and documentation

## Requirements

- A Python version compatible with the dependencies in `requirements.txt`
- A configured Discord bot
- The required bot permissions for moderation and role management

The **Message Content Intent** and **Server Members Intent** must be enabled in the Discord Developer Portal.

## Installation

### 1. Clone the repository

```powershell
git clone https://github.com/CWhymann/python-projekte.git
cd python-projekte
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` in the project root and add your Discord bot token:

```env
DISCORD_TOKEN=your_discord_bot_token
```

Replace the placeholder with your actual token. Never share it or publish it on GitHub.

### 5. Start the bot

```powershell
python bot.py
```

On startup, the bot creates the required SQLite tables in the local database `bot_data.db`.

## Project Structure

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

### Additional Scripts

- `check_db.py` – displays existing database tables and selected records.
- `set_level.py` – sets a user's level. `USER_ID` and `LEVEL` must be checked and adjusted in the script before running it.
- `main.py` – separate Python practice program.
- `utils/hallo.py` – contains a reusable greeting function.

The files `.env`, `.venv/`, `__pycache__/`, and `bot_data.db` are excluded from version control via `.gitignore`.

## Learning Objectives

- Apply Python in a structured way
- Communicate with an external API
- Use events and asynchronous functions
- Persist data with SQLite
- Implement custom commands and permission checks
- Manage configuration and secrets separately
- Document changes traceably with Git

---

<p align="center">
  <sub>Python learning project · Developer Akademie</sub>
</p>