import sqlite3 as sql
import random as r
from funkcije_encription import *
conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = """
    DROP TABLE IF EXISTS wallets;
    CREATE TABLE wallets (
	wallet_id VARCHAR(50),
    coin_id VARCHAR(15),
    quantity numeric(15,6)
    );
    """
    cur.executescript(querry)
    querry = """
    SELECT user_id FROM users
    """
    le_tabelus = cur.execute(querry).fetchall()
    querry = """
    SELECT coin_id FROM coins
    """
    coins = cur.execute(querry).fetchall()
    for _ in range(500):
        id = r.choice(le_tabelus)
        coin_id = r.choice(coins)[0]
        quantaty = r.randrange(0,10000)/100
        le_hash = id_to_hash(id[0])
        querry = """
        INSERT INTO wallets
        (wallet_id,coin_id,quantity)
        VALUES(?,?,?)
        """
        cur.execute(querry,(le_hash,coin_id,quantaty))
    
    
    
    