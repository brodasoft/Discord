import sqlite3

conn = sqlite3.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT
             )''')

rows = c.fetchall()
for row in rows:
    print(row)

conn.close()