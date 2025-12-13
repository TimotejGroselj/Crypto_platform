import sqlite3 as sql
import matplotlib.pyplot as plt
import requests
from PIL import Image
import io
import time
from datetime import datetime

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

        self.coin_name,self.coin_img = self.cur.execute(querry,(self.coin_id,)).fetchall()[0]

    def get_prices(self):
        querry = """
            SELECT date, price FROM coins_prices
            WHERE coin_id = ?
            """
        le_data=self.cur.execute(querry,(self.coin_id,)).fetchall()
        le_dict = dict()
        for coin_id,quantity in le_data:
            le_dict[coin_id] = quantity
        return le_dict
    def get_coin_id(self):
        return self.coin_id
    def get_coin_name(self):
        return self.coin_name
    def get_coin_img(self):
        img = Image.open(io.BytesIO(requests.get(self.coin_img).content)) #i have searched the stack exchange for an hour to find this bad boi
        return img

    def draw_graph(self):
        le_data = self.get_prices()
        fig, ax = plt.subplots()
        fig.set_figwidth(15)
        fig.set_figheight(7)
        ax.plot(le_data.keys(), le_data.values())
        ax.set_xticks(range(0,len(le_data), len(le_data)//5))
        ax.set_xlabel("date")
        ax.set_ylabel("EUR per coin")#to poprav ce se ti ne zdi prou
        ax_image = fig.add_axes([0.9,0.9,0.1,0.1])
        ax_image.imshow(self.get_coin_img())
        ax_image.axis("off")
        ax.text(1.01,0.95,f"latest price\n{round(self.get_prices()[max(self.get_prices().keys())],6)}",transform=ax.transAxes)
        ax.text(1.01,0.85,f"best price\n{round(max(self.get_prices().values()),6)}",transform=ax.transAxes)
        plt.show()
        
