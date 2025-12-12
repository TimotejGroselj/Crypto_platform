import sqlite3 as sql
from funkcije_encription import *
import random


"""
NOTE:
CE BOS ZALAUFU TA FILE POL MORS TUD USE PODATKE V TABELAH POSODOBIT!
"""

conn = sql.connect('cryptodata.sqlite')
command = """
        DROP TABLE IF EXISTS coins;
        CREATE TABLE coins (
           coin_id varchar(15) PRIMARY KEY,
           coin_name text NOT NULL UNIQUE,
           coin_img text NOT NULL
        );
        DROP TABLE IF EXISTS coins_prices;
        CREATE TABLE coins_prices (
          coin_id varchar(15),
          date date NOT NULL,
          price numeric(15,6) NOT NULL,
          PRIMARY KEY (coin_id, date)
        );
        DROP TABLE IF EXISTS assets;
        CREATE TABLE assets (
            wallet_id varchar(50),
            coin_id varchar(15),
            money numeric(15,6) NOT NULL,
            PRIMARY KEY (wallet_id, coin_id)
        );
        """
with conn:
    cur = conn.cursor()
    cur.executescript(command)
    querry = "SELECT user_id FROM users;"
    le_tabelus = cur.execute(querry).fetchall()
    coins = cur.execute("SELECT coin_id FROM coins;").fetchall()
    for user_id in le_tabelus:
        le_hash = id_to_hash(user_id[0])
        cur.execute("INSERT INTO assets (wallet_id,coin_id,money) VALUES (?,?,?)",
                    [le_hash, 'EUR', round(random.uniform(200, 1000), 2)])
        for coin in coins:
            q2 = "INSERT INTO assets (wallet_id, coin_id,money) VALUES (?,?,?)"
            cur.execute(q2, [le_hash, coin[0], 0])
