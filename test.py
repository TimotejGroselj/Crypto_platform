import sqlite3 as sql
from funkcije_encription import *

conn = sql.connect('cryptodata.sqlite')
with open(f"data.bin", "rb") as data:
    salt = pickle.load(data)
with conn:
    cur = conn.cursor()
    querry = """
    SELECT coin_id,quantity FROM wallets
    WHERE wallet_id = ?
    """
    hash = id_to_hash(27)
    print(hash)
    print(cur.execute(querry,(hash,)).fetchall())
        