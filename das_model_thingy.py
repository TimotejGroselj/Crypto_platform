import subprocess
from class_coin import Coin
from el_assetso import Assets
from el_login import Login





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
            print("Succesful login!")
            return email
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

    
            
                