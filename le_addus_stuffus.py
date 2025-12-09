from das_data import data,get_prices,populars
import sqlite3 as sql
import time
from datetime import datetime


connection = sql.connect("cryptodata.sqlite")
cur = connection.cursor()
with connection:
    try:
        for coin in data: #coinov ne bova dodajala (omejila samo na 10 coinov)
            c1 = "SELECT coin_name FROM coins WHERE coin_id = ?"
            here = cur.execute(c1,[coin['id']])
            if not here:
                command = "INSERT INTO coins (coin_id, coin_name, coin_img) VALUES (?,?,?);"
                cur.execute(command,[coin['id'],coin['name'],coin['image']])
        print("Inserting prices...")
        length = len(populars)
        start = 0
        print(f'Do not abort the process (cca 2.5 minutes) -> grab a coffee :)')
        for coin in populars:
            elstrong = f'Progress: {str((100/length) * start)}%' #progress bar da se nous ukenju :)
            print("$" * start + "-" * (length - start) + ' ' + elstrong)
            dateprice = get_prices(coin)
            for date,price in dateprice:  #date,price za 364 dni nazaj
                date = datetime.fromtimestamp(date/1000).strftime("%Y-%m-%d")
                command = "SELECT date FROM coins_prices WHERE date = ? AND coin_id = ?;"
                here = cur.execute(command,[date,coin]).fetchall()
                if not here:
                    command = "INSERT INTO coins_prices (coin_id, date, price) VALUES (?,?,?);"
                    cur.execute(command, [coin, date, price])
                else:
                    command = "UPDATE coins_prices SET price = ? WHERE coin_id = ? AND date = ?;"
                    cur.execute(command, [price, coin, date])
            start += 1
            time.sleep(15)
        print('$' * length + ' Loading complete!')
    except sql.OperationalError as error:
        print("During the operation, an error occurred:", error)
