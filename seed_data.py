"""
Populates the coins table and coins_prices table, then creates wallet rows
for all existing users. Run once after create_tables.py.
"""
import random
import sqlite3

from crypto_utils import hash_value
from market_api import SUPPORTED_COINS, fetch_coin_metadata
from updater import update_coin_prices


def populate_coins_table() -> None:
    """
    Inserts coin metadata into the coins table.
    Does nothing if the table is already populated.
    """
    conn = sqlite3.connect("cryptodata.sqlite")
    with conn:
        cur = conn.cursor()
        if cur.execute("SELECT coin_id FROM coins").fetchall():
            return  # already populated
        for coin in fetch_coin_metadata():
            cur.execute(
                "INSERT INTO coins (coin_id, coin_name, coin_img) VALUES (?, ?, ?)",
                (coin["id"], coin["name"], coin["image"]),
            )


def create_user_wallets() -> None:
    """
    Creates asset rows (EUR + each coin) for every user in the users table.
    Each user receives a random starting EUR balance between 200 and 1000.
    """
    conn = sqlite3.connect("cryptodata.sqlite")
    with conn:
        cur = conn.cursor()
        user_ids = [row[0] for row in cur.execute("SELECT user_id FROM users").fetchall()]
        coin_ids = [row[0] for row in cur.execute("SELECT coin_id FROM coins").fetchall()]
        for user_id in user_ids:
            wallet_id = hash_value(user_id)
            cur.execute(
                "INSERT INTO assets (wallet_id, coin_id, money) VALUES (?, ?, ?)",
                (wallet_id, "EUR", round(random.uniform(200, 1000), 2)),
            )
            for coin_id in coin_ids:
                cur.execute(
                    "INSERT INTO assets (wallet_id, coin_id, money) VALUES (?, ?, ?)",
                    (wallet_id, coin_id, 0),
                )


if __name__ == "__main__":
    populate_coins_table()

    total = len(SUPPORTED_COINS)
    print("Fetching price history — this takes approximately 2.5 minutes. Please wait.")
    for i, coin_id in enumerate(SUPPORTED_COINS):
        progress = int((100 / total) * i)
        bar = "$" * i + "-" * (total - i)
        print(f"{bar}  {progress}%")
        update_coin_prices(coin_id)
    print("$" * total + "  100% — Done!")

    create_user_wallets()
