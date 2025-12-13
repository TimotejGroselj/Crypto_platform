import sqlite3 as sql
import time
from datetime import datetime
from funkcije_encription import *
import random
from updater import *
from das_data import data,populars


def assign_wallets():
    """Vsakemu uporabniku poda lastno denarnico"""
    connection = sql.connect("cryptodata.sqlite")
    cur = connection.cursor()
    querry = "SELECT user_id FROM users;"
    le_tabelus = cur.execute(querry).fetchall()
    coins = cur.execute("SELECT coin_id FROM coins;").fetchall()
    with connection:
        for user_id in le_tabelus:
            le_hash = id_to_hash(user_id[0])
            cur.execute("INSERT INTO assets (wallet_id,coin_id,money) VALUES (?,?,?)",
                        [le_hash, 'EUR', round(random.uniform(200, 1000), 2)])
            for coin in coins:
                q2 = "INSERT INTO assets (wallet_id, coin_id,money) VALUES (?,?,?)"
                cur.execute(q2, [le_hash, coin[0], 0])
    return None


def fill_coins_table():
    """
    Funckija doda kovance v tabelo coins;
    Če so kovanci že v tabeli ne naredi ničesar
    Dodajanje novih kovancev zaenkrat še funkcija ne podpira
    """
    connection = sql.connect("cryptodata.sqlite")
    cur = connection.cursor()
    with connection:
        q1 = "SELECT coin_id FROM coins;"
        coinz = cur.execute(q1).fetchall()
        if not coinz:
            for coin in data:
                q2 = "INSERT INTO coins (coin_id, coin_name, coin_img) VALUES (?,?,?);"
                cur.execute(q2, [coin['id'], coin['name'], coin['image']])
    return None

#prestavu eno fukcijo v drug file ke drgac je blo use funky+ deletu time sleep
fill_coins_table()
length = len(populars)
start = 0
print(f'Do not abort the process (cca 2.5 minutes) -> grab a coffee :)')
for coin in populars:
    elstrong = f'Progress: {str((100 / length) * start)}%'
    print("$" * start + "-" * (length - start) + ' ' + elstrong)
    update_coins_prices(coin)
    start += 1
print('$' * length + ' Loading complete!')
#generate_users()
assign_wallets()
