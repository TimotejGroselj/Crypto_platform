import sqlite3 as sql
import random as r
from funkcije_encription import *
conn = sql.connect('cryptodata.sqlite')

with conn:
    cur = conn.cursor()
    querry = """
    DROP TABLE IF EXISTS transactions;
    CREATE TABLE transactions (
    trans_id integer PRIMARY KEY,
	wallet_id VARCHAR(50),
    coin_id VARCHAR(15),
    quantity numeric(15,6),
    valid integer CHECK (valid in (0,1)),
    type VARCHAR(4) CHECK (type in ('buy','sell'))
    );
    """
    cur.executescript(querry)