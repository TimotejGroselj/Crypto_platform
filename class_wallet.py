import sqlite3 as sql

class Wallet():
    """
    
    """
    def __init__(self, hash:str):
        conn = sql.connect('cryptodata.sqlite') 
        with conn:
            self.cur = conn.cursor()
        self.hash = hash
        querry = """
            SELECT moneh FROM wallets
            WHERE wallet_id = ?
            """
        self.moneh = self.cur.execute(querry,self.hash).fetchone()

    def add_remove_moneh(self,moneh):
        self.moneh += moneh

    def update(self):
        querry = """
        UPDATE wallets SET moneh = ? WHERE wallet_id = ?
        """
        self.cur.execute(querry,(self.moneh,self.hash))

    def get_balance(self):
        querry = """
            SELECT coin_id, quantity FROM balances
            WHERE wallet_id = ?
            """
        le_data=self.cur.execute(querry,(self.hash)).fetchall()
        le_dict = dict()
        for coin_id,quantity in le_data:
            le_dict[coin_id] = quantity
        return le_dict