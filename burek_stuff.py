import sqlite3 as sql
from funkcije_encription import *
import random


conn = sql.connect("cryptodata.sqlite")
cur = conn.cursor()
q1 = """
        DROP TABLE IF EXISTS assets;
        CREATE TABLE assets (
            wallet_id varchar(50),
            coin_id varchar(15),
            money numeric(15,6) NOT NULL,
            PRIMARY KEY (wallet_id, coin_id)
        );"""

qq = "SELECT user_id FROM users WHERE email = ?;"
z = cur.execute(qq,['ecogle0@so-net.ne.jp']).fetchone()[0]
print(z)

if not(0 < 100.5 < 100): print("yep")


with conn:
    cur.executescript(q1)
    querry = "SELECT user_id FROM users;"
    le_tabelus = cur.execute(querry).fetchall()
    coins = cur.execute("SELECT coin_id FROM coins;").fetchall()
    for user_id in le_tabelus:
        le_hash = id_to_hash(user_id[0])
        cur.execute("INSERT INTO assets (wallet_id,coin_id,money) VALUES (?,?,?)", [le_hash,'EUR',round(random.uniform(200, 1000),2)])
        for coin in coins:
            q2 = "INSERT INTO assets (wallet_id, coin_id,money) VALUES (?,?,?)"
            cur.execute(q2, [le_hash, coin[0],0])
