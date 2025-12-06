import sqlite3 as sql

"""
NOTE:
CE BOS ZALAUFU TA FILE POL MORS TUD USE PODATKE V TABELAH POSODOBIT!
"""

conn = sql.connect('cryptodata.sqlite')
command = """
        DROP TABLE IF EXISTS coins;
        CREATE TABLE coins (
           coin_id varchar(15) PRIMARY KEY,
           coin_name text NOT NULL UNIQUE,
           coin_img text NOT NULL
        );
        DROP TABLE IF EXISTS coins_prices;
        CREATE TABLE coins_prices (
          coin_id varchar(15),
          date date NOT NULL,
          price numeric(15,6) NOT NULL,
          PRIMARY KEY (coin_id, date)
        );
        """
with conn:
    cursor = conn.cursor()
    try:
        cursor.executescript(command)
        print("Successfully created coins table!")
    except sql.OperationalError as error:
        print(f"Something went wrong!: {error} ")