import sqlite3 as sql
from funkcije_encription import *
import random


conn = sql.connect("cryptodata.sqlite")
cur = conn.cursor()
qq = "SELECT username FROM users WHERE email = 'monk2@gmail.monk'"
print(cur.execute(qq).fetchone()!=None)
