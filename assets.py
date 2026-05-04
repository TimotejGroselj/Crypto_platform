import sqlite3

from crypto_utils import hash_value


class AssetsManager:
    """
    Handles creation and initialisation of user asset records.
    Used during account registration to set up a wallet for a new user.
    """

    def __init__(self):
        self.conn = sqlite3.connect("cryptodata.sqlite")
        self.cur = self.conn.cursor()

    def create_wallet(self, email: str, initial_eur: float) -> None:
        """
        Creates asset rows for a new user — one EUR row and one row per coin.
        Raises ValueError if initial_eur is negative.
        """
        if initial_eur < 0:
            raise ValueError("Initial EUR balance must be non-negative.")

        user_id = self.cur.execute(
            "SELECT user_id FROM users WHERE email = ?", (email,)
        ).fetchone()[0]
        wallet_id = hash_value(user_id)
        coin_ids = [row[0] for row in self.cur.execute("SELECT coin_id FROM coins").fetchall()]

        with self.conn:
            self.cur.execute(
                "INSERT INTO assets (wallet_id, coin_id, money) VALUES (?, ?, ?)",
                (wallet_id, "EUR", initial_eur),
            )
            for coin_id in coin_ids:
                self.cur.execute(
                    "INSERT INTO assets (wallet_id, coin_id, money) VALUES (?, ?, ?)",
                    (wallet_id, coin_id, 0),
                )
