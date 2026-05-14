import sqlite3
from datetime import datetime, timezone

from market_api import fetch_coin_price_history
import os
from create_tables import *
from seed_data import *

from market_api import SUPPORTED_COINS


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def is_price_current(coin_id: str) -> bool:
    """Returns True if the coin's price data is already up to date for today."""
    with sqlite3.connect("cryptodata.sqlite") as conn:
        last_date = conn.execute(
            "SELECT MAX(date) FROM coins_prices WHERE coin_id = ?", (coin_id,)
        ).fetchone()[0]
    return last_date is not None and _today() <= last_date


def update_coin_prices(coin_id: str) -> None:
    """
    Fetches price history from the API and inserts any missing dates into
    coins_prices. If today's price already exists, it is updated in place.
    """
    
    if is_price_current(coin_id):
        return

    price_history = fetch_coin_price_history(coin_id)

    with sqlite3.connect("cryptodata.sqlite") as conn:
        cur = conn.cursor()
        last_date = cur.execute(
            "SELECT MAX(date) FROM coins_prices WHERE coin_id = ?", (coin_id,)
        ).fetchone()[0] or ""

        prev_date = ""
        for timestamp_ms, price in price_history:
            date_str = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")

            if date_str <= last_date:
                prev_date = date_str
                continue

            if prev_date == date_str:
                cur.execute(
                    "UPDATE coins_prices SET price = ? WHERE coin_id = ? AND date = ?",
                    (price, date_str, coin_id),
                )
            else:
                cur.execute(
                    "INSERT INTO coins_prices (coin_id, date, price) VALUES (?, ?, ?)",
                    (coin_id, date_str, price),
                )
            prev_date = date_str

def update_all_prices() -> None:
    """Checks if each coin's price data is current, and updates it if not."""
    total = len(SUPPORTED_COINS)
    print("Fetching price history — this takes approximately 2.5 minutes if not updated. Please wait.")
    for i, coin_id in enumerate(SUPPORTED_COINS):
        progress = int((100 / total) * i)
        bar = "$" * i + "-" * (total - i)
        print(f"{bar}  {progress}%")
        update_coin_prices(coin_id)
    print("$" * total + "  100% — Done!")
            
def check_database() -> None:
    """
    Checks if the database file exists. If not, runs the seed scripts to create the database and populate it with initial data. Then checks if each coin's price data is current, and updates it if not.
    """
    
    if not os.path.exists("cryptodata.sqlite"):
        print("Creating database...")
        create_tables()

    with sqlite3.connect("cryptodata.sqlite") as conn:
        test = conn.execute("SELECT * FROM coins").fetchone()
    if test is None:
        print("Populating coins table...")
        populate_coins_table()

    update_all_prices()

    with sqlite3.connect("cryptodata.sqlite") as conn:
        test = conn.execute("SELECT * FROM assets").fetchone()
    if test is None:
        print("Creating user wallets...")
        create_user_wallets()

    with sqlite3.connect("cryptodata.sqlite") as conn:
        test = conn.execute("SELECT * FROM transactions").fetchone()
    if test is None:
        print("Seeding transactions...")
        seed_transactions()
            
