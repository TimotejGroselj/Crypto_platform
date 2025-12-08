from das_data import data,get_prices,populars
import sqlite3 as sql
import time
from datetime import datetime


connection = sql.connect("cryptodata.sqlite")
cur = connection.cursor()
with connection:
    try:
        for coin in data: #coinov ne bova dodajala (omejila samo na 10 coinov)
            command = "INSERT INTO coins (coin_id, coin_name, coin_img) VALUES (?,?,?);"
            cur.execute(command,[coin['id'],coin['name'],coin['image']])
        print("Successfully inserted coins")
    except sql.IntegrityError as error:
        print(f"Coins already updated: {error}")
    print("Inserting prices...")
    length = len(populars)
    start = 0
    print(f'Do not abort the process (cca 2.5 minutes) -> grab a coffee :)')
    for coin in populars:
        elstrong = f'Progress: {str(10 * start)}%' #progress bar da se nous ukenju :)
        print("$" * start + "-" * (length - start) + ' ' + elstrong)
        dateprice = get_prices(coin)
        for date,price in dateprice:  #date,price za 364 dni nazaj
            date = datetime.fromtimestamp(date/1000).strftime("%Y-%m-%d")
            try: #preveri za vsak date, če smo updatal tabelo za ta datum
                command = "INSERT INTO coins_prices (coin_id, date, price) VALUES (?,?,?);"
                cur.execute(command,[coin,date,price])
            except sql.IntegrityError as error: pass
        start += 1
        time.sleep(15)
    print('$' * length + ' Loading complete!')

