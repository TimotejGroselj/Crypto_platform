import subprocess
from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import sqlite3 as sql
from class_user import User

def get_coins():
    conn = sql.connect('cryptodata.sqlite') 
    with conn:
        cur = conn.cursor()
        querry = """
        SELECT coin_id FROM coins
        """
        coins_ids = cur.execute(querry).fetchall()
        coins = []
        for coin_id in coins_ids:
            coins.append(Coin(coin_id[0]))
        return coins


def show_graph(coins):
    """
    
    """
    string = "Which coin do you wish to see:\n"
    for i,coin in enumerate(coins):
        string += f"{i+1}. {coin.get_coin_name()}\n"
    which_one = input(string)
    coins[int(which_one)-1].draw_graph()
    
def do_login():
    """
    Izvede login
    """
    login = Login()
    while True:
        email = input("Enter email adress: ")
        if login.is_user(email):
            break
        else:
            try_again = input("This email addres is not in our database.\n1. Try again\n2. Leave\n")
            if int(try_again) == 1:
                continue
            if int(try_again) == 2:
                return None
    while True:
        password = input("Enter password: ")
        if login.valid_login(email,password):
            user = User(email)
            print(f"Succesful login! Hello {user.get_username()}. ")
            return user
        else:
            try_again = input("Incorect password!\n1. Try again\n2. Leave\n")
            if int(try_again) == 1:
                continue    
            if int(try_again) == 2:
                return None
            
            
def do_register():
    login = Login()
    name = input("Enter your username: ")
    while True:
        email = input("Enter email adress: ")
        if not login.valid_email(email):
            try_again = input("This email addres is invalid.\n1. Try again\n2. Leave\n")
            if int(try_again) == 1:
                continue
            if int(try_again) == 2:
                return False
        else:
            break
            
        if not login.is_user(email):
            break
        else:
            try_again = input("This email addres is already in our database.\n1. Try again\n2. Leave\n")
            if int(try_again) == 1:
                continue
            if int(try_again) == 2:
                return False
    while True:
        password = input("Enter password: ")
        what_worng = login.valid_password(password)
        if what_worng == None:
            print("Account sucesfully added")
            login.create_user(name,email,password)
            ass = Assets()
            money = input("How much do you wish to invest right away (write the amount of money in EUR that will be available for later trading): ")
            if int(money) < 0:
                money = 0
            else: 
                money = int(money) 
            ass.add_assets(email,money)
            return True
        else:
            try_again = input(f"Password must contain at least 2 of {what_worng}\n1. Try again\n2. Leave\n")
            if int(try_again) == 1:
                continue    
            if int(try_again) == 2:
                return False      




            
                