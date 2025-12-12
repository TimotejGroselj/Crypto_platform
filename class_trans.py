import sqlite3 as sql
from funkcije_encription import *
from datetime import datetime
import time
from class_wallet import Wallet

class Transactions():
    """
    
    """
    def __init__(self, wallet_id, coin_id, quantity, type, date = datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d")):
        self.wallet_id = wallet_id
        self.coin_id = coin_id
        self.quantity = quantity
        self.type =type
        self.date = date
        self.valid = "?"
    
    def insert_failed_trans(self):
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
            self.valid = 0
            cur.execute(querry,(self.wallet_id,self.coin_id,self.quantity,self.date,self.valid,self.type))
            
    def insert_succesful_trans(self,new_balance, new_quantity):
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
            self.valid = 1
            cur.execute(querry, (self.wallet_id,self.coin_id,self.quantity,self.date,self.valid,self.type))
            querry = """
            UPDATE balances SET quantity = ? WHERE wallet_id = ? AND coin_id = ?
            """
            cur.execute(querry,(new_quantity, self.wallet_id,self.coin_id))
            

    def izvedi_transakcijo(self):
        """
        Stori transakcijo na wallet 
        """
        conn = sql.connect('cryptodata.sqlite')
        with conn:
            cur = conn.cursor()
            querry = """
            SELECT moneh FROM wallets
            WHERE wallet_id = ?
            """
            moneh = cur.execute(querry,self.wallet_id).fetchone()
            querry = """
            SELECT coin_id from coins
            WHERE coin_id = ?
            """
            a_obstaja = cur.execute(querry,(self.coin_id,)).fetchone()
            if a_obstaja == None:
                self.insert_failed_trans(self,self.wallet_id,self.coin_id,self.quantity,self.type,self.date)
                return None
            querry = """
            SELECT price from coins_prices
            WHERE coin_id = ? AND date = ?
            """
            coin_price = cur.execute(querry,(self.coin_id,self.date)).fetchone()
            #PRODPOSTAVMO DA SO PODATKI POSODBLJENI
            used_moneh = coin_price*self.quantity
    
            querry = """
            SELECT quantity FROM balances
            WHERE wallet_id = ? AND coin_id = ?
            """
            how_many = cur.execute(querry,(self.wallet_id,self.coin_id)).fetchone()
            if type == 'sell':
                if how_many == None or how_many < self.quantity:
                    self.insert_failed_trans(self,self.wallet_id,self.coin_id,self.quantity,self.type,self.date)
                    return None
                else:
                    new_balance = moneh+used_moneh
                    new_quantity = how_many - self.quantity
                    self.insert_succesful_trans(self,self.wallet_id,self.coin_id,self.quantity,self.type,self.date,new_balance, new_quantity)
                    return True
            if moneh == None or moneh < used_moneh:
                self.insert_failed_trans(self,self.wallet_id,self.coin_id,self.quantity,self.type,self.date)
                return None
            else:
                new_balance = moneh-used_moneh
                new_quantity = how_many + self.quantity
                self.insert_succesful_trans(self,self.wallet_id,self.coin_id,self.quantity,self.type,self.date,new_balance, new_quantity)
                return True
            
    def get_trans_coin_id(self):
        return self.coin_id
    def get_trans_wallet_id(self):
        return self.wallet_id
    def get_type(self):
        return self.type
    def get_valid(self):
        return self.valid