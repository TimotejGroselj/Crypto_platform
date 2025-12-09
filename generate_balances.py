import sqlite3 as sql
import random as r
from funkcije_encription import *
conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = """
    DROP TABLE IF EXISTS balances;
    CREATE TABLE balances (
	wallet_id VARCHAR(50),
    coin_id VARCHAR(15),
    quantity numeric(15,6),
    FOREIGN KEY(wallet_id) REFERENCES wallets(wallet_id)
    );
    """
    cur.executescript(querry)
    querry = """
    SELECT wallet_id FROM wallets
    """
    le_tabelus = cur.execute(querry).fetchall()
    querry = """
    SELECT coin_id FROM coins
    """
    coins = cur.execute(querry).fetchall()
    for wallet_id in le_tabelus:
        for coin_id in coins:
            if r.random()>0.5:
                quantaty = r.randrange(0,10000)/100
            else:
                quantaty = 0
            querry = """
            INSERT INTO balances
            (wallet_id,coin_id,quantity)
            VALUES(?,?,?)
            """
            cur.execute(querry,(wallet_id[0],coin_id[0],quantaty))
        
    
    
    