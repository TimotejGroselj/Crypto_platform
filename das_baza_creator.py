import sqlite3 as sql
from das_data import data,get_prices
import time
from datetime import datetime
connection = sql.connect("coin_data.db")
cur = connection.cursor()
with connection:
    query = """
    DROP TABLE IF EXISTS coins;
    CREATE TABLE coins (
    id_coin text PRIMARY KEY,
    name text NOT NULL
    );"""
    cur.executescript(query)

    for coin in data:
        name = coin["name"]
        id = coin["id"]
        query = f"""
                INSERT INTO coins
                (id_coin,name)
                VALUES(?,?);
                """
        cur.execute(query, (id,name))
    
    query = """
    SELECT id_coin FROM coins;
    """
    cur.execute(query)
    coin_ids = cur.fetchall()
    print(coin_ids)
    '''
    for coin_id in coin_ids:
        time.sleep(15)
        print("Working please wait...")
        coin_prices = get_prices(coin_id)
        query = """
        DROP TABLE IF EXISTS 
        ?;
        CREATE TABLE ? (
        price integer,
        date text
        );
        """
        cur.execute(query, (coin_id,coin_id))
        for price,date in coin_prices:
            date = datetime.fromtimestamp(date)
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO ?
            (price,date)
            VALUES(?,?)
            """
            cur.execute(query,(coin_id,price,date))
        '''
        


