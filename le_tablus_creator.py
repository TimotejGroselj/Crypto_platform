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
    try:
        cur.executescript(command)
        print("Success")
    except sql.OperationalError as e:
        print(f"An error occurred: {e}")

