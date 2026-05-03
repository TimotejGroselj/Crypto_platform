import sqlite3
from datetime import datetime, timezone

from market_api import fetch_coin_price_history


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def is_price_current(coin_id: str) -> bool:
    """Returns True if the coin's price data is already up to date for today."""
    conn = sqlite3.connect("cryptodata.sqlite")
    with conn:
        cur = conn.cursor()
        last_date = cur.execute(
            "SELECT MAX(date) FROM coins_prices WHERE coin_id = ?", (coin_id,)
        ).fetchone()[0]
    return last_date is not None and _today() <= last_date


def update_coin_prices(coin_id: str) -> None:
    """
    Fetches price history from the API and inserts any missing dates into
    coins_prices. If today's price already exists, it is updated in place.
    """
    conn = sqlite3.connect("cryptodata.sqlite")
    cur = conn.cursor()

    price_history = fetch_coin_price_history(coin_id)

    with conn:
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
