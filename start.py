import subprocess
from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import os
#from le_addus_stuffus import update_coins_prices
from das_model_thingy import * #tuki so vse funkcije ki jih tle uporablaš tuki NE SMEVA KLICAT NČ SQL

if not os.path.exists("cryptodata.sqlite"):
    subprocess.run(["python","generato_uporabnik.py"])
    subprocess.run(["python","le_tablus_creator.py"])
    subprocess.run(["python","le_addus_stuffus.py"])
    subprocess.run(["python","generato_trans.py"])
    

#update_coins_prices() morm se spisat


print("Hello user!")
print("Most of the user interface is done with the use of numbers. Just enter the number next to the option you wish to do if there is a number.")
while True:
    is_user = input("Do you already have an account?\n1. Yes\n2. No\n")
    if int(is_user) == 1:
        mail = do_login() #rabimo da vrne mail da vemo s kom delamo vse naprej
        if mail != None:
            break
        else:
            continue
    if int(is_user) == 2:
        do_register() #ne rabimo nič kr zmer ko ustvariš account te fukne nazaj na login screan in to se tle zgodi
    
        
    