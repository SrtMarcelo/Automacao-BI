import sqlite3

conn = sqlite3.connect("banco.db")
tabelas = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("Tabelas encontradas no banco:", tabelas)
conn.close()
