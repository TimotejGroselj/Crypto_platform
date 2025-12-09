import sqlite3 as sql
from funkcije_encription import *
import random as r
conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = """
    DROP TABLE IF EXISTS wallets;
    CREATE TABLE wallets (
	wallet_id VARCHAR(50) PRIMARY KEY,
    moneh numeric(15,6)
    );
    """
    cur.executescript(querry)
    querry = """
    SELECT user_id FROM users
    """
    le_tabelus = cur.execute(querry).fetchall()
    for user_id in le_tabelus:
        le_hash = id_to_hash(user_id[0])
        print(le_hash)
        
        querry = """
        INSERT INTO wallets
        (wallet_id,moneh)
        VALUES(?,?)
        """
        cur.execute(querry,(le_hash,r.uniform(0,100000)))
        