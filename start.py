import subprocess
from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import os
from updater import *
from das_model_thingy import * #tuki so vse funkcije ki jih tle uporablaš tuki NE SMEVA KLICAT NČ SQL

#if not os.path.exists("cryptodata.sqlite"):
#    subprocess.run(["python","generato_uporabnik.py"])
#    subprocess.run(["python","le_tablus_creator.py"])
#    subprocess.run(["python","le_addus_stuffus.py"])
#    subprocess.run(["python","generato_trans.py"])
coins_ids = get_coins()
#for coin in coins_ids:
#    if not is_updated(coin):
#        update_coins_prices(coin)
coins = []
for coin_id in coins_ids:
    coins.append(Coin(coin_id[0]))



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
        string = "Which coin do you wish to see:\n"
        for i,coin in enumerate(coins):
            string += f"{i+1}. {coin.get_coin_name()}\n"
        which_one = input(string)
        coins[int(which_one)-1].draw_graph()
    if int(what_to_do) == 3:
        assets = user.check_assets()
        for coin, quant in assets.items():
            print(f"{coin.get_coin_name()}: {quant}")
    if int(what_to_do) == 4:
        money = input("How much do you wish to deposit (this money will be available for commiting transactions): ")
        user.change_eur(int(money))
        
    if int(what_to_do) == 5:
        while True:
            money = int(input("How much do you wish to take out (this money was eaither deposited to the account or acquired through selling): "))
            if not user.change_eur(-money):
                try_again = input("You cant take out more than you own!\n1. Try again\n2. Leave\n")
                if int(try_again) == 1:
                    continue
                if int(try_again) == 2:
                    break
            else:
                break
    if int(what_to_do) == 6:
        pass
    if int(what_to_do) == 7:
        break
        
        
        


        
    