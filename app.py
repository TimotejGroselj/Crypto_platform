import os
import uuid
import subprocess
from bottle import redirect, request, response, route, run, static_file, template
import json
import threading
from market_api import SUPPORTED_COINS  # needed so we know coins_total
from auth import AuthManager
from coin import Coin
from updater import is_price_current, update_coin_prices
from services import get_all_coins
from user import User

# In-memory session store: {session_id: email}
_sessions: dict[str, str] = {}
_setup_state: dict = {
    "status": "idle",  # idle | starting | seeding_users | seeding_coins
    # | fetching_prices | creating_wallets | done
    "coins_done": 0,
    "coins_total": 0,
    "current_coin": "",
}
#change

def _require_session() -> str:
    """Returns the email for the current session, or redirects to login."""
    session_id = request.cookies.get("session_id")
    email = _sessions.get(session_id)
    if not email:
        redirect("/")
    return email


# ------------------------------------------------------------------
# Static assets
# ------------------------------------------------------------------

@route("/static/<filename>")
def serve_static(filename):
    return static_file(filename, root="./static")


@route("/temp/<filename>")
def serve_temp(filename):
    return static_file(filename, root="./temp")


# ------------------------------------------------------------------
# Auth routes
# ------------------------------------------------------------------

@route("/")
def show_login(): #change
    if not os.path.exists("cryptodata.sqlite"):
        # Only kick off seeding once
        if _setup_state["status"] == "idle":
            _setup_state["status"] = "starting"
            threading.Thread(target=_run_setup, daemon=True).start()
        return template("setup")

    return template("login", error=None, email=None, password=None)


@route("/login", method="POST")
def handle_login():
    email = request.forms.get("email")
    password = request.forms.get("password")
    auth = AuthManager()

    if not auth.is_valid_email(email):
        return template("login", error="Please enter a valid email address.", email=None, password=None)
    if not auth.is_registered(email):
        return template("login", error="No account found for this email.", email=email, password=None)
    if not auth.check_password(email, password):
        return template("login", error="Incorrect password.", email=email, password=None)

    session_id = str(uuid.uuid4())
    _sessions[session_id] = email
    response.set_cookie("session_id", session_id, secure=False, httponly=True, samesite="Lax")
    return redirect("/greet")


@route("/register")
def show_register():
    suggested_password = AuthManager().generate_password()
    return template("register", error=None, username=None, email=None, password=suggested_password)


@route("/register", method="POST")
def handle_register():
    username = request.forms.get("username")
    email = request.forms.get("email")
    password = request.forms.get("password")
    confirm_password = request.forms.get("confirm_password")
    initial_eur = int(request.forms.get("assets", 0))
    auth = AuthManager()
    if not auth.is_valid_email(email):
        return template("register", error="Invalid email address.", username=username, email=None, password=password)
    if auth.is_registered(email):
        return template("register", error="An account with this email already exists.", username=username, email=email, password=password)
    if auth.validate_password(password) is not None:
        return template("register", error="Please choose a stronger password.", username=username, email=email, password=None)
    if password != confirm_password:
        return template("register", error="Passwords do not match.", username=username, email=email, password=password)

    auth.create_user(username, email, password)
    user = User(email)
    user.initialise_wallet(max(initial_eur, 0.01))
    return redirect("/")


@route("/logout")
def handle_logout():
    session_id = request.cookies.get("session_id")
    _sessions.pop(session_id, None)
    response.delete_cookie("session_id")
    for pic in os.listdir("temp"):
        os.remove(f"temp/{pic}")
    return redirect("/")


# ------------------------------------------------------------------
# Authenticated pages
# ------------------------------------------------------------------

@route("/greet")
def show_greeting():
    email = _require_session()
    username = User(email).get_username()
    return template("success", name=username)


@route("/dashboard")
def show_dashboard():
    email = _require_session()
    coins = get_all_coins()
    for coin in coins:
        if not is_price_current(coin.get_coin_id()):
            update_coin_prices(coin.get_coin_id())

    coin_data = {
        coin.get_coin_id(): {
            "logo": coin.get_coin_img_url(),
            "name": coin.get_coin_name(),
            "price": coin.get_todays_price(),
            "change": coin.get_daily_change_pct(),
        }
        for coin in coins
    }
    return template("dashboard", box_el=coin_data)


@route("/account")
def show_account():
    email = _require_session()
    user = User(email)
    return _render_account(user, flash=None, flash_type=None)


@route("/account/eur", method="POST")
def handle_eur_adjustment():
    email = _require_session()
    user = User(email)
    action = request.forms.get("action")
    try:
        amount = float(request.forms.get("amount", 0))
    except ValueError:
        amount = 0.0

    if amount <= 0:
        flash, flash_type = "Please enter a valid amount.", "err"
    elif action == "deposit":
        user.adjust_eur_balance(amount)
        flash, flash_type = f"Successfully deposited €{round(amount, 2)}.", "ok"
    elif action == "withdraw":
        if user.adjust_eur_balance(-amount):
            flash, flash_type = f"Successfully withdrew €{round(amount, 2)}.", "ok"
        else:
            flash, flash_type = "Insufficient EUR balance.", "err"
    else:
        flash, flash_type = "Unknown action.", "err"

    return _render_account(user, flash=flash, flash_type=flash_type)


def _render_account(user: User, flash, flash_type):
    """Builds the context dict and renders the account template."""
    email = _require_session()
    balances = user.get_balances()
    eur_balance = balances.pop("EUR", 0)

    coin_map = {c.get_coin_id(): c for c in get_all_coins()}
    holdings = {}
    total_value = eur_balance

    for coin_id, amount in balances.items():
        coin = coin_map.get(coin_id)
        if coin is None:
            continue
        price = coin.get_todays_price()
        value_eur = amount * price
        total_value += value_eur
        holdings[coin_id] = {
            "name": coin.get_coin_name(),
            "logo": coin.get_coin_img_url(),
            "amount": amount,
            "price": price,
            "value_eur": value_eur,
        }

    return template(
        "account",
        username=user.get_username(),
        email=user.email,
        eur_balance=eur_balance,
        total_value=total_value,
        holdings=holdings,
        transactions=user.get_transaction_history(),
        flash=flash,
        flash_type=flash_type,
    )


@route("/coin/<coin_id>")
def show_coin(coin_id):
    email = _require_session()
    user = User(email)
    coin = Coin(coin_id)
    coin.save_graph()
    balances = user.get_balances()
    return template(
        "coin",
        coin_id=coin_id,
        coin_name=coin.get_coin_name(),
        coin_logo=coin.get_coin_img_url(),
        price=coin.get_todays_price(),
        change=coin.get_daily_change_pct(),
        balance=balances.get("EUR", 0),
        holdings=balances.get(coin_id, 0),
        flash=None,
        flash_type=None,
    )


@route("/coin/<coin_id>/trade", method="POST")
def handle_trade(coin_id):
    email = _require_session()
    user = User(email)
    coin = Coin(coin_id)
    action = request.forms.get("action", "buy")

    try:
        amount = float(request.forms.get("amount", 0))
    except (ValueError, TypeError):
        amount = 0.0

    balances = user.get_balances()
    eur_balance = balances.get("EUR", 0)
    coin_holdings = balances.get(coin_id, 0)
    price = coin.get_todays_price()

    if amount <= 0:
        flash, flash_type = "Please enter a valid amount.", "err"
    elif action == "buy":
        cost = amount * price
        if cost > eur_balance:
            flash, flash_type = "Insufficient EUR balance.", "err"
        else:
            pct = (cost / eur_balance) * 100 if eur_balance > 0 else 0
            ok = user.execute_trade(pct, 1, coin)
            flash = f"Bought {round(amount, 6)} {coin.get_coin_name()}." if ok else "Trade failed."
            flash_type = "ok" if ok else "err"
    elif action == "sell":
        if amount > coin_holdings:
            flash, flash_type = "Insufficient coin holdings.", "err"
        else:
            pct = (amount / coin_holdings) * 100 if coin_holdings > 0 else 0
            ok = user.execute_trade(pct, 0, coin)
            flash = f"Sold {round(amount, 6)} {coin.get_coin_name()}." if ok else "Trade failed."
            flash_type = "ok" if ok else "err"
    else:
        flash, flash_type = "Unknown action.", "err"

    coin.save_graph()
    updated = user.get_balances()
    return template(
        "coin",
        coin_id=coin_id,
        coin_name=coin.get_coin_name(),
        coin_logo=coin.get_coin_img_url(),
        price=price,
        change=coin.get_daily_change_pct(),
        balance=updated.get("EUR", 0),
        holdings=updated.get(coin_id, 0),
        flash=flash,
        flash_type=flash_type,
    )


@route("/setup/status")
def setup_status(): #change
    """Polled by setup.html every 1.5 s to report real seeding progress."""
    response.content_type = "application/json"
    return json.dumps(_setup_state)


def _run_setup(): #change
    """
    Runs every seeding step in order, updating _setup_state as it goes
    so the frontend can display accurate progress.
    """
    # -- step 1: seed users --
    _setup_state["status"] = "seeding_users"
    subprocess.run(["python", "seed_users.py"], check=True)

    # -- step 2: create tables + coin metadata --
    _setup_state["status"] = "seeding_coins"
    subprocess.run(["python", "create_tables.py"], check=True)

    # populate coins table inline so we can track per-coin price progress
    from seed_data import populate_coins_table
    populate_coins_table()

    # -- step 3: fetch price history coin by coin --
    from market_api import SUPPORTED_COINS
    from updater import update_coin_prices

    _setup_state["status"] = "fetching_prices"
    _setup_state["coins_total"] = len(SUPPORTED_COINS)
    _setup_state["coins_done"] = 0

    for coin_id in SUPPORTED_COINS:
        _setup_state["current_coin"] = coin_id
        update_coin_prices(coin_id)
        _setup_state["coins_done"] += 1

    _setup_state["current_coin"] = ""

    # -- step 4: create wallets --
    _setup_state["status"] = "creating_wallets"
    from seed_data import create_user_wallets
    create_user_wallets()

    # -- step 5: seed transactions (optional, keep if you use it) --
    subprocess.run(["python", "seed_transactions.py"], check=True)

    # -- done --
    _setup_state["status"] = "done"


if __name__ == "__main__":
    run(host="127.0.0.1", port=8080, debug=True)
