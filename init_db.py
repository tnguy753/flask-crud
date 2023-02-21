import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (name, points) VALUES (?, ?)",
            ('Thao Nguyen', '90')
            )

cur.execute("INSERT INTO posts (name, points) VALUES (?, ?)",
            ('Duc Nguyuen', '70')
            )

connection.commit()
connection.close()