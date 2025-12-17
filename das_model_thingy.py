
from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import sqlite3 as sql
from class_user import *



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
    which_one = int_input(string+f"{len(coins)+1}. Leave\n",len(coins)+1)
    if which_one == len(coins)+1:
        return 
    coins[int(which_one)-1].draw_graph()
    
def show_today_prices(coins):
    i = 1
    for coin in coins:
        print(f"{i}. {coin.get_coin_name()}:\n\tprice: {coin.get_todays_price()}\n\tchange from yesterday: {round(coin.get_change(),6)}%")
        i += 1
    
def show_market(coin:Coin, how_far_back = 364):
    """
    
    """
    conn = sql.connect('cryptodata.sqlite') 
    with conn:
        cur = conn.cursor()
        querry = """
        SELECT date,quantity FROM transactions
        WHERE coin_id = ? AND type = 'buy' AND valid = 1
        ORDER BY date DESC
        """
        buying = cur.execute(querry, (coin.get_coin_id(),)).fetchall()
        
        querry = """
        SELECT date,quantity FROM transactions
        WHERE coin_id = ? AND type = 'sell' AND valid = 1
        ORDER BY date DESC
        """
        selling = cur.execute(querry, (coin.get_coin_id(),)).fetchall()

        querry = """
        SELECT date FROM coins_prices
        GROUP BY date
        ORDER BY date DESC limit ?
        """
        dates = cur.execute(querry,(how_far_back,)).fetchall()
        dates = [el[0] for el in dates]
        data_for_every_day = dict()
        for date in dates:
            data_for_every_day[date] = [0,0]
            
        for date,quant in buying:
            if date in data_for_every_day:
                data_for_every_day[date][0] +=quant

        for date,quant in selling:
            if date in data_for_every_day:
                data_for_every_day[date][1] +=quant
        
        
        print(f"{'Sold volume':<12}{'|':^3}{'Date':^12}{'|':^3}{'Bought volume':<12}")
        sold_volume = 0
        bought_volume = 0
        for i, date in enumerate(dates):
            sold = data_for_every_day[date][1]
            bought = data_for_every_day[date][0]
            sold_volume += sold
            bought_volume += bought
            print(f"{round(sold,5):^12}{'|':^3}{date:^12}{'|':^3}{round(bought,5):^12}")
            if i >=how_far_back:
                break
            
        all_volume = sold_volume+bought_volume
        if all_volume == 0:
            print(f"Nothing happend in the last {how_far_back} days")
        else:
            sold_volume,bought_volume = (sold_volume/all_volume)*100,(bought_volume/all_volume)*100   
            print(f"Total market change in the last {how_far_back} days:")
            print(f"{round(sold_volume,2):>49}% : {round(bought_volume,2)}%")
            print("-"*int(sold_volume)+"+"*int(bought_volume))
            
def do_show_market():
    """
    
    """
    data = get_coins()
    tabelus = []
    i = 1
    string = ""
    for coin in data:
        tabelus.append(coin)
        string += f"{i}. {coin.get_coin_name()}\n"
        i += 1
    
    which_one = int_input("Which coin do you want to see?\n"+string+f"{len(tabelus)+1}. Leave\n", len(tabelus)+1)
    if which_one == len(tabelus)+1:
        return
    how_far_back = int_input("For how many days bacl do you want to see the changes to the market volumes (if nothing or invalid is entered deafult is maximum 364 days): ",364)
    if how_far_back == 364:
        show_market(tabelus[which_one-1],364)
    else:
        show_market(tabelus[which_one-1],how_far_back)
    
    
    
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
            try_again = int_input("This email addres is not in our database.\n1. Try again\n2. Leave\n",2)
            if try_again == 1:
                continue
            if try_again == 2:
                return None
    while True:
        password = input("Enter password: ")
        if login.valid_login(email,password):
            user = User(email)
            print(f"Succesful login! Hello {user.get_username()}. ")
            return user
        else:
            try_again = int_input("Incorect password!\n1. Try again\n2. Leave\n",2)
            if try_again == 1:
                continue    
            if try_again == 2 or try_again == -1:
                return None
            
            
def do_register():
    login = Login()
    name = input("Enter your username: ")
    while True:
        email = input("Enter email adress: ")
        if not login.valid_email(email):
            try_again = int_input("This email addres is invalid.\n1. Try again\n2. Leave\n",2)
            if try_again == 1:
                continue
            if try_again == 2:
                return False
        elif not login.is_user(email):
            break
        else:
            try_again = int_input("This email addres is already in our database.\n1. Try again\n2. Leave\n",2)
            if try_again == 1:
                continue
            if try_again == 2:
                return False
    while True:
        password = input("Enter password: ")
        what_worng = login.valid_password(password)
        if what_worng == None:
            print("Account sucesfully added")
            login.create_user(name,email,password)
            ass = Assets()
            money = float_input("How much do you wish to invest right away (write the amount of money in EUR that will be available for later trading, invalid input will result in starting balance 0): ")
            if money -1:
                money = 0
            else: 
                money = money
            ass.add_assets(email,money)
            return True
        else:
            try_again = int_input(f"Password must contain at least 2 of {what_worng}\n1. Try again\n2. Leave\n",2)
            if int(try_again) == 1:
                continue    
            if int(try_again) == 2:
                return False      

    



            
                