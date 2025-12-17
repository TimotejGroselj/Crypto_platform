import sqlite3 as sql
from funkcije_encription import id_to_hash

conn = sql.connect('cryptodata.sqlite') 
with conn:
    cur = conn.cursor()
    
print(cur.execute(f"SELECT * FROM transactions WHERE wallet_id = ?", (id_to_hash(101),)).fetchall()) 