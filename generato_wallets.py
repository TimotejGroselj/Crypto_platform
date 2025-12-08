import sqlite3 as sql
import bcrypt as by
import random as r
import pickle
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
    with open(f"data.bin", "rb") as data:
        salt = pickle.load(data)
    for _ in range(500):
        id = r.choice(le_tabelus)
        coin_id = r.choice(coins)[0]
        quantaty = r.randrange(0,10000)/100
        id = str(id[0]).encode('utf-8')
        le_hash = by.hashpw(id,salt).decode('utf-8')
        querry = """
        INSERT INTO wallets
        (wallet_id,coin_id,quantity)
        VALUES(?,?,?)
        """
        cur.execute(querry,(le_hash,coin_id,quantaty))
    
    
    
    