import time
from datetime import datetime
import sqlite3 as sql



print("2025-12-12">'')

print(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d'))

today = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
connection = sql.connect("cryptodata.sqlite")
cur = connection.cursor()
with connection:
    q1 = "SELECT date FROM coins_prices WHERE date = ?;"
    print(cur.execute(q1,['2025-12-09']).fetchall())

if not [1]:
    print('dad')
