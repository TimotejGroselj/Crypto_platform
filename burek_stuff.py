from class_user import *
from el_login import *
import sqlite3 as sql


l = Login()

#l.create_user('Bizo','bizo@gmail.com','12abAB')

conn = sql.connect('cryptodata.sqlite')
cur = conn.cursor()

q1 = "SELECT * FROM users WHERE email = 'bizo@gmail.com'"
q2 = "SELECT"
with conn:
    en = cur.execute(q1).fetchall()
    gmail = en[0][2]
    user = User(gmail)
    #user.add_assets(100)
    user.show_assets()
