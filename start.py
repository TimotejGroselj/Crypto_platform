import subprocess
from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import os
from updater import *
from das_model_thingy import * #tuki so vse funkcije ki jih tle uporablaš tuki NE SMEVA KLICAT NČ SQL

if not os.path.exists("cryptodata.sqlite"):
    subprocess.run(["python","generato_uporabnik.py"])
    subprocess.run(["python","le_tablus_creator.py"])
    subprocess.run(["python","le_addus_stuffus.py"])
    subprocess.run(["python","generato_trans.py"])
coins = get_coins()
for coin in coins:
   if not is_updated(coin.get_coin_id()):
        update_coins_prices(coin.get_coin_id())



print("Hello user!")
print("Most of the user interface is done with the use of numbers. Just enter the number next to the option you wish to do if there is a number.")
cond = True
while True:
    is_user = input("Do you already have an account?\n1. Yes\n2. No\n3. Leave\n")
    if int(is_user) == 1:
        user = do_login() #rabimo da vrne mail da vemo s kom delamo vse naprej
        if user != None:
            break
        else:
            continue
    if int(is_user) == 2:
        do_register() #ne rabimo nič kr zmer ko ustvariš account te fukne nazaj na login screan in to se tle zgodi1
    if int(is_user) == 3:
        cond = False
        break
    
while cond:
    what_to_do = input("What do you want to do today?\n1. See todays prices\n2. See a price graph of cryptocurrency\n3. Look at your assets\n4. Deposit money\n5. Take money out\n6. Commit a transaction \n7. Leave\n")
    if int(what_to_do) == 1:
        pass
    if int(what_to_do) == 2:
        show_graph(coins)
    if int(what_to_do) == 3:
        user.show_assets()
    if int(what_to_do) == 4:
        user.deposit()
    if int(what_to_do) == 5:
        user.take_out()
    if int(what_to_do) == 6:
        user.do_buy_sell()
    if int(what_to_do) == 7:
        break
        
        
        


        
    