import sqlite3

connection = sqlite3.connect('./../data/database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS data (
id INTEGER PRIMARY KEY,
coin_hand INTEGER NOT NULL,
coin_bank INTEGER NOT NULL,
diamond INTEGER NOT NULL
)
''')

connection.commit()
connection.close()