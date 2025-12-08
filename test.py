import sqlite3 as sql
import bcrypt as by
import random as r
import pickle
conn = sql.connect('cryptodata.sqlite')
with open(f"data.bin", "rb") as data:
    salt = pickle.load(data)
with conn:
    cur = conn.cursor()
    querry = """
    SELECT coin_id,quantity FROM wallets
    WHERE wallet_id = ?
    """
    id = 30
    id = str(id).encode('utf-8')
    hash = by.hashpw(id,salt).decode('utf-8')
    print(hash)
    print(cur.execute(querry,(hash,)).fetchall())
        