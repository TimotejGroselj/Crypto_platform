from das_data import data,get_prices,populars
import sqlite3 as sql
import time
from datetime import datetime
from funkcije_encription import *
import random


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


def update_coins_prices(coin):
    """
    Funkcija doda nove cene za dani kovanec od zadnjega znanega datuma v coins_prices;
    Če so cene posodobljene do današnjega datuma spremeni ceno današnjega datuma v ceno, ki je trenutna
    """
    connection = sql.connect("cryptodata.sqlite")
    cur = connection.cursor()
    dateprice = get_prices(coin)
    with connection:
        q1 = "SELECT MAX(date) FROM coins_prices WHERE coin_id = ?;" #dobimo zadnji datum, ki je biu updatan
        last_date = cur.execute(q1,[coin]).fetchone()[0]
        if not last_date: last_date = '' #če slučajn ni nobenga datuma not
        yesterday = ''
        for date,price in dateprice:
            real_date = datetime.fromtimestamp(date/1000).strftime("%Y-%m-%d")
            if real_date <= last_date:
                continue
            else:
                if yesterday == real_date:
                    q2 = "UPDATE coins_prices SET price = ? WHERE coin_id = ? AND date = ?;"
                    cur.execute(q2, [price, real_date, coin])
                else:
                    q3 = "INSERT INTO coins_prices (coin_id,date,price) VALUES(?,?,?);"
                    cur.execute(q3,[coin,real_date,price])
            yesterday = real_date
    return None

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
