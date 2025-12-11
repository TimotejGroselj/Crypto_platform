import sqlite3 as sql

class Coin():
    """
    
    """
    def __init__(self, coin_id):
        conn = sql.connect('cryptodata.sqlite') 
        with conn:
            self.cur = conn.cursor()
        self.coin_id = coin_id
        querry = """
        SELECT coin_name, coin_img FROM coins
        WHERE coin_id = ?
        """
        self.coin_name,self.coin_img = self.cur.execute(querry).fetchall()

    def get_prices(self):
        querry = """
            SELECT date, price FROM coins_prices
            WHERE coin_id = ?
            """
        le_data=self.cur.execute(querry,(self.coin_id)).fetchall()
        le_dict = dict()
        for coin_id,quantity in le_data:
            le_dict[coin_id] = quantity
        return le_dict
    def get_coin_id(self):
        return self.coin_id
    def get_coin_name(self):
        return self.coin_name
    def get_coin_img(self):
        return self.coin_img