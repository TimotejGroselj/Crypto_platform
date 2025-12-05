from das_data import data,get_prices
import sqlite3 as sql
import time
from datetime import datetime


connection = sql.connect("cryptodata.sqlite")
cur = connection.cursor()
with connection:
    try:
        table_ids = []
        for coin in data: #dodaj kovance
            command = "INSERT INTO coins (coin_id, coin_name, coin_img) VALUES (?,?,?);"
            cur.execute(command,[coin['id'],coin['name'],coin['image']])
            table_ids.append(coin['id'])
        print("Successfully inserted coins")
        print("Inserting prices...")
        length = len(table_ids)
        start = 0
        print(f'Do not abort the process -> grab a coffee :)')
        for coin in table_ids: #date,price za 364 dni nazaj
            time.sleep(15)
            elstrong = f'Progress: {str(10 * start)}%' #progress bar da se nous ukenju :)
            print("$" * start + "-" * (length - start) + ' ' + elstrong)
            dateprice = get_prices(coin)
            for date,price in dateprice:
                date = datetime.fromtimestamp(date/1000)
                command = "INSERT INTO coins_prices (coin_id, date, price) VALUES (?,?,?);"
                cur.execute(command,[coin,date,price])
            start += 1
        print('$' * length + ' Loading complete!')
    except sql.IntegrityError as error: #če pride do tega (seprau mas ze kovance not) updati sam trenutn dan price od coinov
        print(f"This coin already exists in coins: {error}")
        print("Checking today's price")
        """
        DANASNJI PRICUS SE PA BO
        today = datetime.today().strftime('%Y-%m-%d')
        check = cur.execute("SELECT * FROM coins_prices WHERE date = ?",[today]).fetchall()
        if check:
            print("Price already updated!")
        else:
            print("Inserting today's price...")
            names = cur.execute("SELECT coin_id FROM coins").fetchall()
            for id in names:
                command = "INSERT INTO coins_prices (coin_id, date, price) VALUES (?,?,?);"
                cur.execute(command,[id[0],today,price])
        """


zapisi = cur.execute("SELECT coin_id FROM coins").fetchall() #Test da so res zrihtani
print(zapisi)
for d in zapisi:
    print(d)


pogoj = cur.execute("SELECT * FROM coins WHERE coin_id = ?",['bitcoin']).fetchall()
if pogoj:
    print('Date exists!')
else:
    print('Date doesn\'t exist!')
