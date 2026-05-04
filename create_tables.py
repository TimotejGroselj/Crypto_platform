"""
Creates the database schema from scratch.
WARNING: Running this script drops all existing tables and their data.
You must re-run seed_users.py, seed_data.py, and seed_transactions.py afterwards.
"""
import sqlite3

DDL = """
DROP TABLE IF EXISTS coins;
CREATE TABLE coins (
    coin_id   VARCHAR(15) PRIMARY KEY,
    coin_name TEXT        NOT NULL UNIQUE,
    coin_img  TEXT        NOT NULL
);

DROP TABLE IF EXISTS coins_prices;
CREATE TABLE coins_prices (
    coin_id VARCHAR(15)     NOT NULL,
    date    DATE            NOT NULL,
    price   NUMERIC(15, 6)  NOT NULL,
    PRIMARY KEY (coin_id, date)
);

DROP TABLE IF EXISTS assets;
CREATE TABLE assets (
    wallet_id VARCHAR(50)    NOT NULL,
    coin_id   VARCHAR(15)    NOT NULL,
    money     NUMERIC(15, 6) NOT NULL,
    PRIMARY KEY (wallet_id, coin_id)
);
"""

conn = sqlite3.connect("cryptodata.sqlite")
with conn:
    cur = conn.cursor()
    try:
        cur.executescript(DDL)
        print("Tables created successfully.")
    except sqlite3.OperationalError as e:
        print(f"Error creating tables: {e}")
