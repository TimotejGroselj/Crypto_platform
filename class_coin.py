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
        if self.coin_id != "EUR":
            querry = """
            SELECT coin_name, coin_img FROM coins
            WHERE coin_id = ?
            """
            data = self.cur.execute(querry,(self.coin_id,)).fetchall()[0]
            self.coin_name = data[0]
            self.coin_img = data[1]
        else:
            self.coin_name = "EUR"
            self.coin_img = None
    def get_prices(self):
        querry = """
            SELECT date, price FROM coins_prices
            WHERE coin_id = ?
            """
        le_data=self.cur.execute(querry,(self.coin_id,)).fetchall()
        le_dict = dict()
        for date,quantity in le_data:
            le_dict[date] = quantity
        return le_dict
    def get_todays_price(self):
        querry = """
            SELECT price FROM coins_prices
            WHERE coin_id = ? and date = (SELECT MAX(date) FROM coins_prices WHERE coin_id = ?)
            """
        return self.cur.execute(querry,(self.coin_id,self.coin_id)).fetchone()[0]
    def get_change(self):
        """
        
        """
        today = self.get_todays_price()
        yesterday = datetime.fromtimestamp(time.time()-86400).strftime("%Y-%m-%d")
        querry = """
            SELECT price FROM coins_prices
            WHERE coin_id = ? and date = ?
            """
        yesterday = self.cur.execute(querry, (self.coin_id,yesterday)).fetchone()[0]
        return (today*100)/yesterday-100
        
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
        fig.set_facecolor("black")
        ax.set_facecolor("black")
        #ax.imshow(we decide le backround image)
        ax.set_xticks(range(0,len(le_data), len(le_data)//12))
        ax.set_xlabel("date")
        ax.set_ylabel("EUR per coin")#to poprav ce se ti ne zdi prou
        
        ax.xaxis.label.set_color('white')        
        ax.yaxis.label.set_color('white')          
        ax.tick_params(axis='x', colors='white')    
        ax.tick_params(axis='y', colors='white')  
        ax.spines['left'].set_color('white')        
        ax.spines['top'].set_color('white')       
        ax.spines['right'].set_color('white')        
        ax.spines['bottom'].set_color('white')     
          
        difs = [[],[]]
        for i in range(len(le_data.values())-1):
            dif = list(le_data.values())[i+1]-list(le_data.values())[i]
            if dif>0:
                difs[0].append(0)
                difs[1].append(dif)
            else:
                difs[0].append(-dif)
                difs[1].append(0)
        ax.errorbar(list(le_data.keys())[:-1],list(le_data.values())[:-1],yerr=difs,color = "lightgreen",ecolor="orangered")
        
        ax_image = fig.add_axes([0.9,0.9,0.1,0.1])
        ax_image.imshow(self.get_coin_img())
        ax_image.axis("off")
        #le_font = nasledn text kopiran iz offical website tko da veva iz kje dobiva font Matplotlib also provides an option to offload text rendering to a TeX engine (usetex=True), see Text rendering with LaTeX.
        #also link: https://matplotlib.org/stable/users/explain/text/usetex.html#usetex
        latest = self.get_prices()[max(self.get_prices().keys())]
        best = max(self.get_prices().values())
        dif = (best/latest)*100
        ax.text(1.01,0.90,f"latest price\n{round(latest,6)}\n-{round(dif,2)}% from best",transform=ax.transAxes,color = "red")
        ax.text(1.01,0.80,f"best price\n{round(best,6)}",transform=ax.transAxes, color = "green")
        #i can add abunch more stuff sam mi mors povedat kaj bi zgledal kulll pa prav za pc spletno stran
        plt.show()
        
