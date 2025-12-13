import subprocess
from class_coin import Coin
from el_assetso import Assets
from el_login import Login
import os
from le_addus_stuffus import update_coins_prices
from das_model_thingy import * #tuki so vse funkcije ki jih tle uporablaš tuki NE SMEVA KLICAT NČ SQL

if os.path.exists("cryptodata.sqlite"):
    subprocess.run(["python","generato_uporabnik.py"])
    subprocess.run(["python","le_tablus_creator.py"])
    subprocess.run(["python","le_addus_stuffus.py"])
    subprocess.run(["python","generato_trans.py"])



update_coins_prices()
print("Hello user!")
print("Most of the user interface is done with the use of numbers. Just enter the number next to the option you wish to do if there is a number.")
while True:
    is_user = input("Do you already have an account?\n1. Yes\n2. No")
    while True:
        login = Login()
        if int(is_user) == 1:
            email = input("Enter email adress: ")
            geslo = input("Enter geslo: ")
            if not login.is_user(email):
                try_again = input("This email is not in our database. Do you wish to\n1. Try again\n2. Create a account")
                if int(try_again) == 1:
                    continue
                if int(try_again) == 2:
                    break
                else:
                    