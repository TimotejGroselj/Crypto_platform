import sqlite3 as sql
from funkcije_encription import *
from class_coin import Coin
from datetime import datetime
import time
import re
from inputs import *


class User:
    def __init__(self, email):
        self.email = email
        self.conn = sql.connect('cryptodata.sqlite')
        with self.conn:
            self.cur = self.conn.cursor()
            querry = """
            SELECT user_id, username FROM users
            WHERE email = ?
            """
            self.id, self.username = self.cur.execute(querry, (self.email,)).fetchall()[0]      
            
    
    
    ### fn za za displayat stvari
    def get_username(self):
        return self.username
    def show_assets(self):
        """
    
        """
        assets = self.check_assets()
        for coin, quant in assets.items():
            print(f"{coin.get_coin_name()}: {quant}")
            
            

            
    ### funkcije za spremembe direkt u sql
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

    def change_eur(self,money):
        """Naloži si EUR na račun"""
        eur = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ?", [id_to_hash(self.id)]).fetchone()[0]
        if money < 0 and eur<abs(money):
            return False
        with self.conn:
            q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR';"
            self.cur.execute(q1,[money+eur,id_to_hash(self.id)])
        return True

    def check_assets(self):
        """Vrne slovar, koliko denarja imaš v posameznih valutah"""
        q2 = "SELECT coin_id,money FROM assets WHERE wallet_id = ?"
        name = self.cur.execute(q2,[id_to_hash(self.id)]).fetchall()
        assets = dict()
        for coin,money in name:
            assets[Coin(coin)] = money
        return assets
    
    ### funkciji za transakcije izvajat
    def data_collect_for_trans(self,id):
        """
        sam funkcija za pobrat podatke o trans
        """
        tabelus = []
        i = 1
        string = ""
        data = self.check_assets()
        for coin, quant in data.items():
            item = (coin,quant)
            tabelus.append(item)
            string += f"{i}. {item[0].get_coin_name()}: {item[1]}\n"
            i += 1
        if id == 0:
            which_one = int_input("Which coin do you want to sell?\n"+string+f"{len(tabelus)+1}. Leave\n", len(tabelus)+1)
            if which_one == len(tabelus)+1:
                return (-1,-1)
            how_much = float_input(r"How much do you want to sell (enter an amount in %. The inputed % of the cryptocurrency owned will be sold, invalid input will set this to 0): ")
        else:
            which_one = int_input("In which coin do you want to invest?\n"+string+f"{len(tabelus)+1}. Leave\n", len(tabelus)+1)
            if which_one == len(tabelus)+1:
                return (-1,-1)
            how_much = float_input(r"How much do you want to invest (enter an amount in %. The inputed % of your investable money will be invested, invalid input will set this to 0): ")
        return (tabelus[which_one-1][0],how_much)
        
        
    def buy_sell(self,amount,invest_id,coin:Coin):
        """Amount je koliko % [0.01,1] od svojega EUR denarja želiš vložiti oz koliko % od svojga kovanca hočs prodt,
         invest_id = 1 -> če kups,0 -> če prodaš"""
        with self.conn:
            if amount > 100 or amount < 0:
                print("Invalid amount!")
                querry = """
                INSERT INTO transactions
                (wallet_id,coin_id,quantity,date,valid,type)
                VALUES(?,?,?,?,?,?)
                """
                self.cur.execute(querry,(id_to_hash(self.id),coin.get_coin_id(),amount*self.check_assets()[Coin("EUR")]/100,datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"),0,"sell" if invest_id==0 else "buy"))
                return False
            eur = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ? AND coin_id = 'EUR';", [id_to_hash(self.id)]).fetchone()[0]
            coin_currently = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ? AND coin_id = ?", [id_to_hash(self.id),coin.get_coin_id()]).fetchone()[0]
            coin_price = coin.get_todays_price()
            q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?;"
            q2 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR';"
            if invest_id == 1:
                invest = (eur*(amount/100))/coin_price
                self.cur.execute(q1,[coin_currently+invest,id_to_hash(self.id),coin.get_coin_id()])
                self.change_eur(-eur*amount/100)
                self.cur.execute(q2,[eur - eur*amount/100,id_to_hash(self.id)])
            else:
                invest = (coin_currently*(amount/100))*coin_price
                self.change_eur(invest)
                self.cur.execute(q1,[coin_currently-(coin_currently*amount/100),id_to_hash(self.id),coin.get_coin_id()])
                self.cur.execute(q2, [eur + invest, id_to_hash(self.id)])
            querry = """
            INSERT INTO transactions
            (wallet_id,coin_id,quantity,date,valid,type)
            VALUES(?,?,?,?,?,?)
            """
            self.cur.execute(querry,(id_to_hash(self.id),coin.get_coin_id(),eur*amount/100 if invest_id == 1 else (coin_currently*(amount/100))*coin_price,datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d"),1,"sell" if invest_id==0 else "buy"))
        return True


  
    
    ### funkcije za pobiranje podatku od userja 
    def deposit(self):
        money = float_input("How much do you wish to deposit: ")
        self.change_eur(money)
        
    def take_out(self):
        while True:
            money = float_input("How much do you wish to take out (this money was eaither deposited to the account or acquired through selling): ")
            if not self.change_eur(-money):
                try_again = int_input("You cant take out more than you own!\n1. Try again\n2. Leave\n", 2)
                if int(try_again) == 1:
                    continue
                if int(try_again) == 2:
                    break
            else:
                break

    def do_buy_sell(self):
        """
        
        """
        what_u_doin = int_input("Do you want to sell or buy cryptocurrency?\n1. Buy\n2. Sell\n3. Leave\n",3)
        if what_u_doin == 1:
            coin,how_much_u_wanna_sell = self.data_collect_for_trans(1)
            if coin == -1:
                return False
            return self.buy_sell(how_much_u_wanna_sell,1,coin)
        if what_u_doin == 2:
            coin,how_much_u_wanna_sell = self.data_collect_for_trans(0)
            if coin == -1:
                return False
            return self.buy_sell(how_much_u_wanna_sell,0,coin)
        if what_u_doin == 3:
            return False
        

            
    
            