import sqlite3 as sql
from das_data import data
connection = sql.connect("coin_data.db")
cur = connection.cursor()
query = """
DROP TABLE IF EXISTS coins;
CREATE TABLE coins (
id_coin text PRIMARY KEY,
name text NOT NULL
);"""
cur.executescript(query)

for coin in data:
    name = coin["name"]
    id = coin["id"]
    query = f"""
            INSERT INTO coins
            (id_coin,name)
            VALUES('{id}','{name}')
        """
    cur.execute(query)



