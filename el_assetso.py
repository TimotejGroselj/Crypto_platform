import sqlite3 as sql
from funkcije_encription import *


class Assets:
    def __init__(self):
        self.conn = sql.connect("cryptodata.sqlite")
        self.cur = self.conn.cursor()

    def add_assets(self,email,eur):
        """Za novega uporabnika ustvari kripto denarnico"""
        if eur <= 0: raise ValueError("EUR must be greater than 0")
        q1 = "SELECT user_id FROM users WHERE email = ?"
        id = self.cur.execute(q1,[email]).fetchone()[0]
        hash = id_to_hash(id)
        coins = self.cur.execute("SELECT coin_id FROM coins;").fetchall()
        with self.conn:
            self.cur.execute("INSERT INTO assets (wallet_id,coin_id,money) VALUES (?,?,?)",[hash, 'EUR',eur])
            for coin in coins:
                q2 = "INSERT INTO assets (wallet_id, coin_id,money) VALUES (?,?,?)"
                self.cur.execute(q2, [hash, coin[0], 0])

    def check_assets(self,wallet_id):
        """Vrne slovar, koliko denarja imaš v posameznih valutah"""
        q2 = "SELECT coin_id,money FROM assets WHERE wallet_id = ?"
        name = self.cur.execute(q2,[wallet_id]).fetchall()
        assets = dict()
        for coin,money in name:
            assets[coin] = money
        return assets

    def add_eur(self,wallet_id,money):
        """Naloži si EUR na račun"""
        eur = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ?", [wallet_id]).fetchone()[0]
        with self.conn:
            q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR';"
            self.cur.execute(q1,[money+eur,wallet_id])


    def buy_sell(self,wallet_id,amount,invest_id,coin,date):
        """Amount je koliko % [0.01,1] od svojega EUR denarja želiš vložiti oz koliko % od svojga kovanca hočs prodt,
         invest_id = 1 -> če kups,0 -> če prodaš"""
        #if not(0 < amount < 100): return 'Invalid amount'
        eur = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ? AND coin_id = 'EUR';", [wallet_id]).fetchone()[0]
        if int(eur) == 0: return "Not enough EUR!"
        coin_currently = self.cur.execute("SELECT money FROM assets WHERE wallet_id = ? AND coin_id = ?", [wallet_id,coin]).fetchone()[0]
        coin_price = self.cur.execute("SELECT price FROM coins_prices WHERE date = ?", [date]).fetchone()[0]
        with self.conn:
            if invest_id == 1:
                invest = (eur*amount)/coin_price
                q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?;"
                self.cur.execute(q1,[coin_currently+invest,wallet_id,coin])
                eur -= eur*amount
                q2 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR';"
                self.cur.execute(q2,[eur,wallet_id])
            else:
                invest = (coin_currently*amount)*coin_price
                self.add_eur(wallet_id,invest)
                coin_currently -= coin_currently*amount
                q1 = "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?;"
                self.cur.execute(q1,[coin_currently-(coin_currently*amount),wallet_id,coin])
        return "Success!"











