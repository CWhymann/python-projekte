import sqlite3

con = sqlite3.connect("bot_data.db")
for (name,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
    anzahl = con.execute(f"SELECT COUNT(*) FROM {name}").fetchone()[0]
    print(name, anzahl, "Zeilen")
    for zeile in con.execute(f"SELECT * FROM {name} LIMIT 5").fetchall():
        print("   ", zeile)
con.close()
