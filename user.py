import sqlite3
from datetime import datetime, timezone

from cli_inputs import get_float_input, get_int_input
from coin import Coin
from crypto_utils import hash_value


class User:
    """Represents an authenticated user and exposes portfolio and trading operations."""

    def __init__(self, email: str):
        self.email = email
        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        row = cur.execute(
            "SELECT user_id, username FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        self.user_id: int = row[0]
        self.username: str = row[1]

    @property
    def _wallet_id(self) -> str:
        return hash_value(self.user_id)

    # ------------------------------------------------------------------
    # Portfolio queries
    # ------------------------------------------------------------------

    def get_username(self) -> str:
        return self.username

    def get_balances(self) -> dict[str, float]:
        """Returns {coin_id: amount} for all assets in this user's wallet."""
        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        rows = cur.execute(
            "SELECT coin_id, money FROM assets WHERE wallet_id = ?",
            (self._wallet_id,),
        ).fetchall()
        conn.close()
        return {coin_id: amount for coin_id, amount in rows}

    def display_assets(self) -> None:
        """Prints a human-readable summary of all held assets."""
        for coin_id, amount in self.get_balances().items():
            name = coin_id if coin_id == "EUR" else Coin(coin_id).get_coin_name()
            print(f"{name}: {amount}")

    def get_transaction_history(self) -> list[tuple]:
        """Returns a list of (coin_name, quantity, date, type) for all valid transactions."""
        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        rows = cur.execute(
            "SELECT coin_id, quantity, date, type FROM transactions "
            "WHERE wallet_id = ? AND valid = 1 ORDER BY date DESC",
            (self._wallet_id,),
        ).fetchall()
        conn.close()
        return [(Coin(coin_id).get_coin_name(), qty, date, tx_type)
                for coin_id, qty, date, tx_type in rows]

    # ------------------------------------------------------------------
    # EUR balance management
    # ------------------------------------------------------------------

    def adjust_eur_balance(self, delta: float) -> bool:
        """
        Adds delta to the EUR balance (negative delta = withdrawal).
        Returns False if a withdrawal would exceed the available balance.
        """
        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        current = cur.execute(
            "SELECT money FROM assets WHERE wallet_id = ? AND coin_id = 'EUR'",
            (self._wallet_id,),
        ).fetchone()[0]
        if delta < 0 and current < abs(delta):
            conn.close()
            return False
        cur.execute(
            "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR'",
            (current + delta, self._wallet_id),
        )
        conn.commit()
        conn.close()
        return True

    # ------------------------------------------------------------------
    # Trading
    # ------------------------------------------------------------------

    def execute_trade(self, percentage: float, action: int, coin: Coin) -> bool:
        """
        Executes a buy or sell trade.

        Args:
            percentage: Percentage of EUR balance to spend (buy) or percentage
                        of coin holdings to sell (sell). Range [0, 100].
            action:     1 = buy, 0 = sell.
            coin:       The Coin to trade.

        Returns True on success, False on failure.
        """
        if not (0 < percentage <= 100):
            print("Invalid percentage amount!")
            self._record_transaction(coin.get_coin_id(), 0, action, valid=False)
            return False

        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        eur = cur.execute(
            "SELECT money FROM assets WHERE wallet_id = ? AND coin_id = 'EUR'",
            (self._wallet_id,),
        ).fetchone()[0]
        coin_holdings = cur.execute(
            "SELECT money FROM assets WHERE wallet_id = ? AND coin_id = ?",
            (self._wallet_id, coin.get_coin_id()),
        ).fetchone()[0]
        coin_price = coin.get_todays_price()

        if action == 1:  # buy
            spend_eur = eur * (percentage / 100)
            coins_acquired = spend_eur / coin_price
            cur.execute(
                "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?",
                (coin_holdings + coins_acquired, self._wallet_id, coin.get_coin_id()),
            )
            cur.execute(
                "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR'",
                (eur - spend_eur, self._wallet_id),
            )
            tx_quantity = spend_eur
        else:  # sell
            coins_sold = coin_holdings * (percentage / 100)
            eur_received = coins_sold * coin_price
            cur.execute(
                "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = ?",
                (coin_holdings - coins_sold, self._wallet_id, coin.get_coin_id()),
            )
            cur.execute(
                "UPDATE assets SET money = ? WHERE wallet_id = ? AND coin_id = 'EUR'",
                (eur + eur_received, self._wallet_id),
            )
            tx_quantity = eur_received

        conn.commit()
        conn.close()
        self._record_transaction(coin.get_coin_id(), tx_quantity, action, valid=True)
        return True

    def _record_transaction(self, coin_id: str, quantity: float, action: int, valid: bool) -> None:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        tx_type = "buy" if action == 1 else "sell"
        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO transactions (wallet_id, coin_id, quantity, date, valid, type) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (self._wallet_id, coin_id, quantity, today, int(valid), tx_type),
        )
        conn.commit()
        conn.close()

    # ------------------------------------------------------------------
    # CLI interaction helpers
    # ------------------------------------------------------------------

    def _pick_coin_and_percentage(self, action: int) -> tuple[Coin | None, float]:
        """
        Prompts the user to choose a coin and a percentage for a trade.
        action: 1 = buy, 0 = sell.
        Returns (Coin, percentage) or (None, -1) if the user exits.
        """
        balances = self.get_balances()
        eur_balance = balances.pop("EUR", 0)
        coins = [(Coin(cid), qty) for cid, qty in balances.items()]

        menu = "".join(f"{i+1}. {c.get_coin_name()}: {qty}\n" for i, (c, qty) in enumerate(coins))
        leave_option = len(coins) + 1
        print(f"Your EUR balance: {eur_balance}")

        if action == 0:
            prompt_coin = f"Which coin do you want to sell?\n{menu}{leave_option}. Leave\n"
            prompt_pct = (
                "How much do you want to sell? "
                "(Enter a % of your holdings: "
            )
        else:
            prompt_coin = f"Which coin do you want to buy?\n{menu}{leave_option}. Leave\n"
            prompt_pct = (
                "How much do you want to invest? "
                "(Enter a % of your EUR balance) "
            )

        choice = get_int_input(prompt_coin, leave_option)
        if choice == leave_option:
            return None, -1

        percentage = get_float_input(prompt_pct, 100)
        return coins[choice - 1][0], percentage

    def prompt_trade(self) -> bool:
        """Interactive CLI flow for buying or selling a coin."""
        action = get_int_input(
            "Do you want to buy or sell cryptocurrency?\n1. Buy\n2. Sell\n3. Leave\n", 3
        )
        if action == 3:
            return False
        trade_type = 1 if action == 1 else 0
        coin, percentage = self._pick_coin_and_percentage(trade_type)
        if coin is None:
            return False
        return self.execute_trade(percentage, trade_type, coin)

    def prompt_deposit(self) -> None:
        amount = get_float_input("How much do you wish to deposit: ")
        self.adjust_eur_balance(amount)

    def prompt_withdraw(self) -> None:
        while True:
            amount = get_float_input("How much do you wish to withdraw: ")
            if not self.adjust_eur_balance(-amount):
                choice = get_int_input(
                    "Insufficient balance!\n1. Try again\n2. Leave\n", 2
                )
                if choice == 2:
                    break
            else:
                break

    def initialise_wallet(self, initial_eur: float) -> None:
        """
        Creates the wallet rows for this user (EUR + one row per coin).
        Should only be called once, immediately after account creation.
        """
        if initial_eur <= 0:
            raise ValueError("Initial EUR balance must be greater than 0.")
        conn = sqlite3.connect("cryptodata.sqlite")
        cur = conn.cursor()
        coin_ids = [row[0] for row in cur.execute("SELECT coin_id FROM coins").fetchall()]
        cur.execute(
            "INSERT INTO assets (wallet_id, coin_id, money) VALUES (?, ?, ?)",
            (self._wallet_id, "EUR", initial_eur),
        )
        for coin_id in coin_ids:
            cur.execute(
                "INSERT INTO assets (wallet_id, coin_id, money) VALUES (?, ?, ?)",
                (self._wallet_id, coin_id, 0),
            )
        conn.commit()
        conn.close()