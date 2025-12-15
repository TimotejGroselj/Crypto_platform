import sqlite3 as sql

conn = sql.connect('cryptodata.sqlite') 
with conn:
    cur = conn.cursor()
    
print(cur.execute("SELECT username FROM users WHERE email = 'g@gmail.com'").fetchone()!= None) 