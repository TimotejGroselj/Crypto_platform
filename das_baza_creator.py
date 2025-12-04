import sqlite3 as sql
from das_data import data
connection = sql.connect("coin_data.db")
cur = connection.cursor()
query = """
IF coins EXISTS 
(CREATE TABLE coins (
id_coin integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL
));"""
cur.execute(query)

for coin in data:
    name = coin["name"]
    query = f"""
            INSERT INTO coins
            (name)
            VALUES({name})
            """
    cur.execute(query)



