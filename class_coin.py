import sqlite3 as sql

class Coin():
    """
    
    """
    def __init__(self, coin_id, coin_name, coin_img):
        self.coin_id = coin_id
        self.coin_name = coin_name
        self.coin_img = coin_img
        conn = sql.connect('cryptodata.sqlite') 
        with conn:
            self.cur = conn.cursor()
    
    def  insert_coin(self):
        command = "INSERT INTO coins (coin_id, coin_name, coin_img) VALUES (?,?,?);"
        self.cur.execute(command,(self.coin_id,self.coin_name,self.coin_img))

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