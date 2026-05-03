"""
Generates realistic-looking synthetic transaction history for all wallets.
Run once after seed_data.py.
"""
import random
import sqlite3

from crypto_utils import hash_value

conn = sqlite3.connect("cryptodata.sqlite")

with conn:
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS transactions;
        CREATE TABLE transactions (
            trans_id  INTEGER PRIMARY KEY,
            wallet_id VARCHAR(50),
            coin_id   VARCHAR(15),
            quantity  NUMERIC(15, 6),
            date      DATE    NOT NULL,
            valid     INTEGER CHECK (valid IN (0, 1)),
            type      VARCHAR(4) CHECK (type IN ('buy', 'sell'))
        );
    """)

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
