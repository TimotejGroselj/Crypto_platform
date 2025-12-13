import sqlite3 as sql
import time
from datetime import datetime
from funkcije_encription import *
import random
from das_data import get_prices

def is_updated(coin):
    conn = sql.connect("cryptodata.sqlite")
    with conn:
        cur = conn.cursor()
        q1 = "SELECT MAX(date) FROM coins_prices WHERE coin_id = ?;" #dobimo zadnji datum, ki je biu updatan
        last_date = cur.execute(q1,coin).fetchone()[0]
        today = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
        if today <=last_date:
            return True
        return False
    
    
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
                pass
            else:
                if yesterday == real_date:
                    q2 = "UPDATE coins_prices SET price = ? WHERE coin_id = ? AND date = ?;"
                    cur.execute(q2, [price, real_date, coin])
                else:
                    q3 = "INSERT INTO coins_prices (coin_id,date,price) VALUES(?,?,?);"
                    cur.execute(q3,[coin,real_date,price])
            yesterday = real_date
    return None

