"""
Populates the coins table and coins_prices table, then creates wallet rows
for all existing users. Run once after create_tables.py.
"""
import random
import sqlite3

from crypto_utils import hash_value
from market_api import SUPPORTED_COINS, fetch_coin_metadata


def populate_coins_table() -> None:
    """
    Inserts coin metadata into the coins table.
    Does nothing if the table is already populated.
    """
    with sqlite3.connect("cryptodata.sqlite") as conn:
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
    with sqlite3.connect("cryptodata.sqlite") as conn:
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

def seed_transactions() -> None:
    
    with sqlite3.connect("cryptodata.sqlite") as conn:
        cur = conn.cursor()

        wallet_ids = [row[0] for row in cur.execute(
            "SELECT wallet_id FROM assets GROUP BY wallet_id"
        ).fetchall()]

        dates = sorted([row[0] for row in cur.execute(
            "SELECT date FROM coins_prices GROUP BY date"
        ).fetchall()])
        date_count = len(dates)

        for wallet_id in wallet_ids:
            holdings = cur.execute(
                "SELECT coin_id, money FROM assets WHERE wallet_id = ? AND coin_id != 'EUR'",
                (wallet_id,),
            ).fetchall()

            for coin_id, final_quantity in holdings:
                num_transactions = random.randint(1, 30)

                # Generate a random sequence of signed quantities that sum to final_quantity
                first_amount = random.uniform(1, 1000)
                running_sum = first_amount
                amounts = [first_amount]
                for _ in range(num_transactions):
                    delta = random.uniform(-running_sum, 1000)
                    running_sum += delta
                    amounts.append(delta)

                # Normalise so the sequence sums to final_quantity
                total = sum(amounts)
                normalised = [a / (total / (final_quantity + 0.1)) for a in amounts]

                earliest_possible_index = -1
                for i in range(num_transactions):
                    date_index = random.randint(earliest_possible_index, date_count - num_transactions + i)
                    earliest_possible_index = date_index
                    qty = normalised[i]
                    tx_type = "sell" if qty < 0 else "buy"

                    cur.execute(
                        "INSERT INTO transactions (wallet_id, coin_id, quantity, date, valid, type) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (wallet_id, coin_id, abs(qty), dates[date_index], 1, tx_type),
                    )

                    # Insert a matching failed transaction every 4th iteration
                    if i % 4 == 0:
                        failed_qty = abs(qty) + random.uniform(0, 100) if qty < 0 else abs(abs(qty) + random.uniform(-100, 100))
                        failed_type = "sell" if qty < 0 else "buy"
                        cur.execute(
                            "INSERT INTO transactions (wallet_id, coin_id, quantity, date, valid, type) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (wallet_id, coin_id, failed_qty, dates[date_index], 0, failed_type),
                        )
