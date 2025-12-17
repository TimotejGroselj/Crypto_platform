import subprocess
import sqlite3 as sql

from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import os

from start import what_to_do
from updater import *
from das_model_thingy import * #tuki so vse funkcije ki jih tle uporablaš tuki NE SMEVA KLICAT NČ SQL
from class_user import int_input

"""
if not os.path.exists("cryptodata.sqlite"):
    subprocess.run(["python","generato_uporabnik.py"])
    subprocess.run(["python","le_tablus_creator.py"])
    subprocess.run(["python","le_addus_stuffus.py"])
    subprocess.run(["python","generato_trans.py"])
"""
coins = get_coins()
for coin in coins:
   if not is_updated(coin.get_coin_id()):
        update_coins_prices(coin.get_coin_id())

connection = sql.connect("cryptodata.sqlite")
cursor = connection.cursor()
with connection:
    command = """
            DROP TABLE IF EXISTS test_log
            CREATE TABLE test_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_or_stuff INTEGER NOT NULL,
            selected INTEGER NOT NULL,
            pass INTEGER NOT NULL CHECK (pass in (0,1)),
            problem VARCHAR(50) NOT NULL
            );
    """




cond = True
num = 1
while True:
    is_user = int_input(num,3)
    #is_user = int_input("Do you already have an account?\n1. Yes\n2. No\n3. Leave\n", 3)
    if is_user == 1:
        user = do_login()  # rabimo da vrne mail da vemo s kom delamo vse naprej
        if user != None:
            break
        else:
            continue
    if is_user == 2:
        do_register()  # ne rabimo nič kr zmer ko ustvariš account te fukne nazaj na login screan in to se tle zgodi1
    if is_user == 3:
        cond = False
        break


big_dummy = "bu@gmail.com"
user = User(big_dummy)
while cond:
    #what_to_do = int_input("What do you want to do today?\n1. See todays prices\n2. See a price graph of cryptocurrency\n3. Look at your assets\n4. Look at coin volume changes\n5. Deposit money\n6. Take money out\n7. Commit a transaction \n8. Leave\n",8)
    what_to_do = int_input(num,3)
    if what_to_do == 1:
        show_today_prices(coins)
    if what_to_do == 2:
        show_graph(coins)
    if what_to_do == 3:
        user.show_assets()
    if what_to_do == 4:
        do_show_market()
    if what_to_do == 5:
        user.deposit()
    if what_to_do == 6:
        user.take_out()
    if what_to_do == 7:
        user.do_buy_sell()
    if what_to_do == 8:
        break