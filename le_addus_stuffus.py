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
        print(f'Do not abort the process (cca 2.5 minutes) -> grab a coffee :)')
        for coin in table_ids: #date,price za 364 dni nazaj
            time.sleep(15)
            elstrong = f'Progress: {str(10 * start)}%' #progress bar da se nous ukenju :)
            print("$" * start + "-" * (length - start) + ' ' + elstrong)
            dateprice = get_prices(coin)
            for date,price in dateprice:
                date = datetime.fromtimestamp(date/1000).strftime("%Y-%m-%d")
                command = "INSERT INTO coins_prices (coin_id, date, price) VALUES (?,?,?);"
                cur.execute(command,[coin,date,price])
            start += 1
        print('$' * length + ' Loading complete!')
    except sql.IntegrityError as error: #če pride do tega (seprau mas ze kovance not) updati sam trenutn dan price od coinov
        print(f"This coin already exists in coins: {error}")
        print("Checking today's price")
        today = datetime.today().strftime('%Y-%m-%d')
        try:
            for info in data:
                curr_price = info['current_price']
                name = info['id']
                command = "INSERT INTO coins_prices (coin_id, date, price) VALUES (?,?,?);"
                cur.execute(command,[name,today,curr_price])
        except sql.IntegrityError as error:
            print(f"Coin has already been updated today: {error}")



gc = cur.execute("SELECT * FROM coins_prices WHERE coin_id = 'ethereum'").fetchall()
for row in gc:
    print(row)

