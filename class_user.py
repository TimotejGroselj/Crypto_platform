import sqlite3 as sql
from funkcije_encription import *
from class_coin import Coin
from datetime import datetime
import time

class User():
    def __init__(self, email):
        self.email = email
        conn = sql.connect('cryptodata.sqlite') 
        with conn:
            self.cur = conn.cursor()
            querry = """
            SELECT user_id, username FROM users
            WHERE email = ?
            """
            self.id, self.username = self.cur.execute(querry, (self.email,)).fetchall()[0]      
    def get_username(self):
        return self.username
    def get_id(self):
        return self.id
    
    def add_assets(self,eur):
        """Za novega uporabnika ustvari kripto denarnico"""
        if eur <= 0: raise ValueError("EUR must be greater than 0")
        q1 = "SELECT user_id FROM users WHERE email = ?"
        id = self.cur.execute(q1,[self.email]).fetchone()[0]
        hash = id_to_hash(id)
        coins = self.cur.execute("SELECT coin_id FROM coins;").fetchall()
        with self.conn:
            self.cur.execute("INSERT INTO assets (wallet_id,coin_id,money) VALUES (?,?,?)",[hash, 'EUR',eur])
            for coin in coins:
                q2 = "INSERT INTO assets (wallet_id, coin_id,money) VALUES (?,?,?)"
                self.cur.execute(q2, [hash, coin[0], 0])

    def check_assets(self):
        """Vrne slovar, koliko denarja imaš v posameznih valutah"""
        q2 = "SELECT coin_id,money FROM assets WHERE wallet_id = ?"
        name = self.cur.execute(q2,[id_to_hash(self.id)]).fetchall()
        assets = dict()
        for coin,money in name:
            assets[Coin(coin)] = money
        return assets

    def change_eur(self,money):
        """Naloži si EUR na račun"""
        eur = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ?", [id_to_hash(self.id)]).fetchone()[0]
        if money < 0 and eur<abs(money):
            return False
        q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR';"
        self.cur.execute(q1,[money+eur,id_to_hash(self.id)])
        return True


    def buy_sell(self,amount,invest_id,coin:Coin):
        """Amount je koliko % [0.01,1] od svojega EUR denarja želiš vložiti oz koliko % od svojga kovanca hočs prodt,
         invest_id = 1 -> če kups,0 -> če prodaš"""
        if amount > 100 or amount < 0:
            print("Invalid amount!")
            querry = """
            INSERT INTO transactions
            (wallet_id,coin_id,quantity,date,valid,type)
            VALUES(?,?,?,?,?,?)
            """
            self.cur.execute(querry,(id_to_hash(self.id),coin.get_coin_id(),amount,datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"),0,"sell" if invest_id==0 else "buy"))
            return False
        eur = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ? AND coin_id = 'EUR';", [id_to_hash(self.id)]).fetchone()[0]
        coin_currently = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ? AND coin_id = ?", [id_to_hash(self.id),coin.get_coin_id()]).fetchone()[0]
        coin_price = coin.get_todays_price()
        if invest_id == 1:
            invest = (eur*amount)/coin_price
            q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?;"
            self.cur.execute(q1,[coin_currently+invest,id_to_hash(self.id),coin.get_coin_id()])
            self.change_eur(id_to_hash(self.id),-eur*amount)
            q2 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR';"
            self.cur.execute(q2,[eur,id_to_hash(self.id)])
        else:
            invest = (coin_currently*amount)*coin_price
            
            q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?;"
            self.cur.execute(q1,[coin_currently-(coin_currently*amount),id_to_hash(self.id),coin.get_coin_id()])
        querry = """
        INSERT INTO transactions
        (wallet_id,coin_id,quantity,date,valid,type)
        VALUES(?,?,?,?,?,?)
        """
        self.cur.execute(querry,(id_to_hash(self.id),coin.get_coin_id(),amount,datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"),1,"sell" if invest_id==0 else "buy"))
        return True

    def take_out(self):
        while True:
            money = int(input("How much do you wish to take out (this money was eaither deposited to the account or acquired through selling): "))
            if not self.change_eur(-money):
                try_again = input("You cant take out more than you own!\n1. Try again\n2. Leave\n")
                if int(try_again) == 1:
                    continue
                if int(try_again) == 2:
                    break
            else:
                break
    def deposit(self):
        money = input("How much do you wish to deposit (this money will be available for commiting transactions): ")
        self.change_eur(int(money))
        
    def show_assets(self):
        """
    
        """
        assets = self.check_assets()
        for coin, quant in assets.items():
            print(f"{coin.get_coin_name()}: {quant}")
    
    def data_collect(self,id):
    
        tabelus = []
        i = 1
        string = ""
        data = self.check_assets()
        for coin, quant in data.items():
            item = (i,coin,quant)
            tabelus.append(item)
            string += f"{item[0]}. {item[1].get_coin_name()}: {item[2]}\n"
            i += 1
        if id == 0:
            which_one = int(input("Which coin do you want to sell?\n"+string))
            how_much = int(input(r"How much do you want to sell (enter an amount in %. The inputed % of the cryptocurrency owned will be sold): "))
        else:
            which_one = int(input("In which coin do you want to invest?\n"+string))
            how_much = int(input(r"How much do you want to invest (enter an amount in %. The inputed % of your investable money will be invested): "))
        return (tabelus[which_one-1][1],how_much)
        
    def do_buy_sell(self):
        """
        
        """
        what_u_doin = int(input("Do you want to sell or buy cryptocurrency?\n1. Buy\n2. Sell\n3. Leave\n"))
        if what_u_doin == 1:
            coin,how_much_u_wanna_sell = self.data_collect(1)
            return self.buy_sell(how_much_u_wanna_sell,1,coin)
        if what_u_doin == 2:
            coin,how_much_u_wanna_sell = self.data_collect(0)
            return self.buy_sell(how_much_u_wanna_sell,0,coin)
        if what_u_doin == 3:
            return False
        

    
            