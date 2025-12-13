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
        #ax.imshow(we decide le backround image)
        
        ax.plot(le_data.keys(), le_data.values(),color = "blue")#določva barvo glede na ozadje
        ax.set_xticks(range(0,len(le_data), len(le_data)//5))
        ax.set_xlabel("date")
        ax.set_ylabel("EUR per coin")#to poprav ce se ti ne zdi prou
        difs = [[],[]]
        for i in range(len(le_data.values())-1):
            dif = list(le_data.values())[i+1]-list(le_data.values())[i]
            if dif>0:
                difs[0].append(0)
                difs[1].append(dif)
            else:
                difs[0].append(-dif)
                difs[1].append(0)
        ax.errorbar(list(le_data.keys())[:-1],list(le_data.values())[:-1],yerr=difs,color = "blue",ecolor="red")
        
        ax_image = fig.add_axes([0.9,0.9,0.1,0.1])
        ax_image.imshow(self.get_coin_img())
        ax_image.axis("off")
        #le_font = nasledn text kopiran iz offical website tko da veva iz kje dobiva font Matplotlib also provides an option to offload text rendering to a TeX engine (usetex=True), see Text rendering with LaTeX.
        #also link: https://matplotlib.org/stable/users/explain/text/usetex.html#usetex
        ax.text(1.01,0.95,f"latest price\n{round(self.get_prices()[max(self.get_prices().keys())],6)}",transform=ax.transAxes)
        ax.text(1.01,0.85,f"best price\n{round(max(self.get_prices().values()),6)}",transform=ax.transAxes)
        #i can add abunch more stuff sam mi mors povedat kaj bi zgledal kulll pa prav za pc spletno stran
        plt.show()
        
coin = Coin("bitcoin")
coin.draw_graph()
print("cock")