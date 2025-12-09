import sqlite3 as sql
from funkcije_encription import *
import random as r
conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = """
    DROP TABLE IF EXISTS balances;
    CREATE TABLE balances (
	wallet_id VARCHAR(50) PRIMARY KEY,
    balance numeric(15,6),
    FOREIGN KEY (wallet_id) REFERENCES wallets(wallet_id)
    );
    """
    cur.executescript(querry)
    querry = """
    SELECT wallet_id FROM wallets
    GROUP BY wallet_id
    """
    wallets = cur.execute(querry).fetchall()
    
    for wallet_id in wallets:
        querry = """
        INSERT INTO balances
        (wallet_id,balance)
        VALUES (?,?)
        """
        cur.execute(querry,(wallet_id[0],r.uniform(0,100000)))
        