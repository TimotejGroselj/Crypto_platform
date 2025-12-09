import sqlite3 as sql
from funkcije_encription import *
from datetime import datetime
import time
def failed_trans(wallet_id,coin_id,quantity,type,date):
    """

    """
    conn = sql.connect('cryptodata.sqlite')
    with conn:
        cur = conn.cursor()
        querry = """
            INSERT INTO transactions
            (wallet_id,coin_id,quantity,date,valid,type)
            VALUES (?,?,?,?,?,?)
            """
        cur.execute(querry,(wallet_id,coin_id,quantity,date,0,type))
def succesful_trans(wallet_id,coin_id,quantity,type,date,new_balance, new_quantity):
    """
    
    """
    conn = sql.connect('cryptodata.sqlite')
    with conn:
        cur = conn.cursor()
        querry = """
            INSERT INTO transactions
            (wallet_id,coin_id,quantity,date,valid,type)
            VALUES (?,?,?,?,?,?)
            """
        cur.execute(querry, (wallet_id,coin_id,quantity,date,1,type))
        querry = """
        UPDATE wallets SET balance = ? WHERE wallet_id = ?
        """
        cur.execute(querry,(new_balance,wallet_id))
        querry = """
        UPDATE balances SET quantity = ? WHERE wallet_id = ? AND coin_id = ?
        """
        cur.execute(querry,(new_quantity, wallet_id,coin_id))

def transakcija(wallet_id,coin_id,quantity,type):
    """
    Stori transakcijo na wallet 
    """
    conn = sql.connect('cryptodata.sqlite')
    with conn:
        cur = conn.cursor()
        date = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")
        querry = """
        SELECT balance FROM wallets
        WHERE wallet_id = ?
        """
        moneh = cur.execute(querry,wallet_id).fetchone()
        querry = """
        SELECT coin_id from coins
        WHERE coin_id = ?
        """
        a_obstaja = cur.execute(querry,(coin_id,)).fetchone()
        if a_obstaja == None:
            failed_trans(wallet_id,coin_id,quantity,type,date)
            return None
        querry = """
        SELECT price from coins_prices
        WHERE coin_id = ? AND date = ?
        """
        coin_price = cur.execute(querry,(coin_id,date)).fetchone()
        #PRODPOSTAVMO DA SO PODATKI POSODBLJENI
        used_moneh = coin_price*quantity
  
        querry = """
        SELECT quantity FROM balances
        WHERE wallet_id = ? AND coin_id = ?
        """
        how_many = cur.execute(querry,(wallet_id,coin_id)).fetchone()
        if type == 'sell':
            if how_many == None or how_many < quantity:
                failed_trans(wallet_id,coin_id,quantity,type,date)
                return None
            else:
                new_balance = moneh+used_moneh
                new_quantity = how_many - quantity
                succesful_trans(wallet_id,coin_id,quantity,type,date,new_balance, new_quantity)
                return True
        if moneh == None or moneh < used_moneh:
            failed_trans(wallet_id,coin_id,quantity,type,date)
            return None
        else:
            new_balance = moneh-used_moneh
            new_quantity = how_many + quantity
            succesful_trans(wallet_id,coin_id,quantity,type,date,new_balance, new_quantity)
            return True
        
