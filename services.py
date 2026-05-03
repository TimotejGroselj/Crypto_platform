import sqlite3

from auth import AuthManager
from cli_inputs import get_float_input, get_int_input
from coin import Coin
from user import User


def get_all_coins() -> list[Coin]:
    """Returns a Coin object for every coin in the database."""
    conn = sqlite3.connect("cryptodata.sqlite")
    with conn:
        coin_ids = [row[0] for row in conn.execute("SELECT coin_id FROM coins").fetchall()]
    return [Coin(cid) for cid in coin_ids]


def display_todays_prices(coins: list[Coin]) -> None:
    """Prints today's price and 24 h change for every coin."""
    for i, coin in enumerate(coins, 1):
        print(
            f"{i}. {coin.get_coin_name()}:\n"
            f"\tPrice: {coin.get_todays_price()}\n"
            f"\t24h change: {round(coin.get_daily_change_pct(), 6)}%"
        )


def prompt_coin_graph(coins: list[Coin]) -> None:
    """Interactively asks the user which coin graph to display."""
    menu = "".join(f"{i+1}. {c.get_coin_name()}\n" for i, c in enumerate(coins))
    leave_option = len(coins) + 1
    choice = get_int_input(f"Which coin do you want to see?\n{menu}{leave_option}. Leave\n", leave_option)
    if choice == leave_option:
        return
    coins[choice - 1].show_graph()


def get_market_volume(coin: Coin, days_back: int = 364) -> tuple[dict, float, float]:
    """
    Calculates buy/sell volume distribution per day for a given coin.

    Returns:
        volume_by_date: {date: [sell_pct, buy_pct]}
        total_sell_pct: overall sell share across the period
        total_buy_pct:  overall buy share across the period
    """
    conn = sqlite3.connect("cryptodata.sqlite")
    with conn:
        cur = conn.cursor()

        buys = cur.execute(
            "SELECT date, quantity FROM transactions "
            "WHERE coin_id = ? AND type = 'buy' AND valid = 1 ORDER BY date DESC",
            (coin.get_coin_id(),),
        ).fetchall()

        sells = cur.execute(
            "SELECT date, quantity FROM transactions "
            "WHERE coin_id = ? AND type = 'sell' AND valid = 1 ORDER BY date DESC",
            (coin.get_coin_id(),),
        ).fetchall()

        dates = [row[0] for row in cur.execute(
            "SELECT date FROM coins_prices GROUP BY date ORDER BY date DESC LIMIT ?",
            (days_back,),
        ).fetchall()]

    volume_by_date = {date: [0.0, 0.0] for date in dates}
    for date, qty in buys:
        if date in volume_by_date:
            volume_by_date[date][1] += qty
    for date, qty in sells:
        if date in volume_by_date:
            volume_by_date[date][0] += qty

    total_sell = total_buy = 0.0
    for date in dates:
        sold, bought = volume_by_date[date]
        day_total = sold + bought
        if day_total:
            volume_by_date[date] = [(sold / day_total) * 100, (bought / day_total) * 100]
        total_sell += volume_by_date[date][0]
        total_buy += volume_by_date[date][1]

    grand_total = total_sell + total_buy
    if grand_total:
        total_sell = (total_sell / grand_total) * 100
        total_buy = (total_buy / grand_total) * 100

    return volume_by_date, total_sell, total_buy


def prompt_market_volume() -> None:
    """Interactive CLI flow to display market volume for a chosen coin and date range."""
    coins = get_all_coins()
    menu = "".join(f"{i+1}. {c.get_coin_name()}\n" for i, c in enumerate(coins))
    leave_option = len(coins) + 1
    choice = get_int_input(
        f"Which coin do you want to see?\n{menu}{leave_option}. Leave\n", leave_option
    )
    if choice == leave_option:
        return

    days_back = get_int_input("How many days back do you want to see? ", 364)
    volume_by_date, total_sell, total_buy = get_market_volume(coins[choice - 1], days_back)

    print(f"{'Sell volume':<12}{'|':^3}{'Date':^12}{'|':^3}{'Buy volume':<12}")
    for date in sorted(volume_by_date):
        sell, buy = volume_by_date[date]
        print(f"{round(sell, 5):^12}{'|':^3}{date:^12}{'|':^3}{round(buy, 5):^12}")
    print("-" * int(total_sell) + "+" * int(total_buy))


# ------------------------------------------------------------------
# Auth flows
# ------------------------------------------------------------------

def run_login() -> User | None:
    """CLI login flow. Returns a User on success, or None if the user exits."""
    auth = AuthManager()
    while True:
        email = input("Enter email address: ")
        if auth.is_registered(email):
            break
        choice = get_int_input("Email not found.\n1. Try again\n2. Leave\n", 2)
        if choice == 2:
            return None

    while True:
        password = input("Enter password: ")
        if auth.check_password(email, password):
            user = User(email)
            print(f"Login successful! Welcome back, {user.get_username()}.")
            return user
        choice = get_int_input("Incorrect password.\n1. Try again\n2. Leave\n", 2)
        if choice in (2, -1):
            return None


def run_register() -> bool:
    """CLI registration flow. Returns True on success, False if the user exits."""
    auth = AuthManager()
    username = input("Enter your username: ")

    while True:
        email = input("Enter email address: ")
        if not auth.is_valid_email(email):
            choice = get_int_input("Invalid email address.\n1. Try again\n2. Leave\n", 2)
            if choice == 2:
                return False
        elif auth.is_registered(email):
            choice = get_int_input("Email already registered.\n1. Try again\n2. Leave\n", 2)
            if choice == 2:
                return False
        else:
            break

    while True:
        password = input("Enter password: ")
        failing = auth.validate_password(password)
        if failing is None:
            initial_eur = get_float_input(
                "How much EUR would you like to deposit right away? "
                "(invalid input defaults to 0): "
            )
            if initial_eur < 0:
                initial_eur = 0.0
            auth.create_user(username, email, password)
            user = User(email)
            user.initialise_wallet(max(initial_eur, 0.01))
            print("Account created successfully!")
            return True
        choice = get_int_input(
            f"Password too weak — needs at least 2 {failing}.\n1. Try again\n2. Leave\n", 2
        )
        if choice == 2:
            return False
