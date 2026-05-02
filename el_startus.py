from bottle import route, run, template, static_file, request, redirect, response
from el_login import *
from class_user import *
from das_model_thingy import *
from updater import *
from class_coin import Coin
import uuid
from PIL import Image
import os
sessions = {}
def check_session():
    """Preveri če ima user trenutno sejo"""
    session_id = request.cookies.get('session_id')
    email = sessions.get(session_id)
    if not email:
        redirect('/')
    return email

@route('/static/<filename>')
def static_files(filename):
    """Ovaj za css fileje"""
    return static_file(filename, root='./static')

@route('/temp/<filename>')
def temp(filename):
    """Ovaj za css fileje"""
    return static_file(filename, root='./temp')

@route('/')
def show_login():
    """Prikaze zacetno login stran"""
    return template('login',error=None,email=None,password=None)

@route('/login', method='POST')
def login_logic():
    """Ko ljudek vnasa zadeve not v login"""
    email = request.forms.get('email')
    password = request.forms.get('password')
    l = Login()
    if not l.valid_email(email):
        return template('login', error='Please insert a valid email!', email=None, password=None)
    if not l.is_user(email):
        return template('login',error='This email does not exist!',email=email,password=None)
    if not l.valid_login(email, password):
        return template('login', error='Incorrect password!', email=email, password=None)
    session_id = str(uuid.uuid4())
    sessions[session_id] = email
    response.set_cookie('session_id', session_id, secure=True, httponly=True)
    return redirect("/greet")


@route("/register")
def register_page():
    """Pokaze stran za ustvarjanje accounta"""
    suggested = Login().generate_password()
    return template('register',error=None,username=None,email = None,password=suggested)

@route("/register", method='POST')
def register_logic():
    """Preveri ce vse stima za ustvarjanje accounta, ce stima pol ga vrne na login"""
    username = request.forms.get('username')
    email = request.forms.get('email')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')
    assets = int(request.forms.get('assets'))
    l = Login()

    if not l.valid_email(email):
        return template('register',error ='Please insert a valid email!',username=username,email=None,password=password)
    if l.is_user(email):
        return template('register',error ='User with that email already exists!',username=username,email=email,password=password)
    valid = l.valid_password(password)
    if valid is not None:
        return template('register',error="Chose a stronger password!",username=username,email=email,password=None)
    if password != confirm_password:
        return template('register',error ='Passwords do not match!',username=username,email=email,password=password)
    l.create_user(username,email,password)
    user = User(email)
    user.add_assets(assets)
    redirect("/")
    return None


@route('/greet')
def greet():
    email = check_session()
    user = User(email).get_username()
    return template("success",name=user)

@route('/dashboard')
def show_dashboard():
    email = check_session()
    user = User(email)
    coins = get_coins()
    for coin in coins:
        if not is_updated(coin.get_coin_id()):
                update_coins_prices(coin.get_coin_id())
    box_el = dict()
    for coin in coins:
        coin:Coin
        box_el[coin.get_coin_id()] = dict(logo = coin.get_coin_img_url(), name = coin.get_coin_name(), price = coin.get_todays_price(),change = coin.get_change())
        
    return template("dashboard", box_el = box_el)

@route("/dashboard", method='POST')
def dashboard_logic():
    check_session()
    return None

@route("/logout")
def logout():
    session_id = request.cookies.get('session_id')
    if session_id in sessions:
        del sessions[session_id]
    response.delete_cookie('session_id')
    for pic in os.listdir("temp"):
        os.remove(f"temp/{pic}")
    redirect("/")

@route('/account')
def show_account():
    email = check_session()
    user = User(email)
    assets = user.check_assets()  # dict: {coin_id: amount, 'EUR': amount}

    eur_balance = assets.pop('EUR', 0)

    # build holdings dict with coin metadata + EUR value
    coins = get_coins()
    coin_map = {c.get_coin_id(): c for c in coins}

    holdings = {}
    total_value = eur_balance
    for coin_id, amount in assets.items():
        coin = coin_map.get(coin_id)
        if coin is None:
            continue
        price = coin.get_todays_price()
        value_eur = amount * price
        total_value += value_eur
        holdings[coin_id] = dict(
            name=coin.get_coin_name(),
            logo=coin.get_coin_img_url(),
            amount=amount,
            price=price,
            value_eur=value_eur,
        )

    transactions = user.all_transactions()  # [(coin_name, quantity, date, type), ...]

    return template(
        'account',
        username=user.get_username(),
        email=email,
        eur_balance=eur_balance,
        total_value=total_value,
        holdings=holdings,
        transactions=transactions,
        flash=None,
        flash_type=None,
    )


@route('/account/eur', method='POST')
def account_eur():
    email = check_session()
    user = User(email)
    action = request.forms.get('action')  # 'deposit' or 'withdraw'
    try:
        amount = float(request.forms.get('amount', 0))
    except ValueError:
        amount = 0

    if amount <= 0:
        flash = "Please enter a valid amount."
        flash_type = "err"
    elif action == 'deposit':
        user.change_eur(amount)
        flash = f"Successfully deposited €{round(amount, 2)}."
        flash_type = "ok"
    elif action == 'withdraw':
        success = user.change_eur(-amount)
        if success:
            flash = f"Successfully withdrew €{round(amount, 2)}."
            flash_type = "ok"
        else:
            flash = "Insufficient EUR balance."
            flash_type = "err"
    else:
        flash = "Unknown action."
        flash_type = "err"

    # re-fetch everything to re-render page
    assets = user.check_assets()
    eur_balance = assets.pop('EUR', 0)

    coins = get_coins()
    coin_map = {c.get_coin_id(): c for c in coins}

    holdings = {}
    total_value = eur_balance
    for coin_id, amount_held in assets.items():
        coin = coin_map.get(coin_id)
        if coin is None:
            continue
        price = coin.get_todays_price()
        value_eur = amount_held * price
        total_value += value_eur
        holdings[coin_id] = dict(
            name=coin.get_coin_name(),
            logo=coin.get_coin_img_url(),
            amount=amount_held,
            price=price,
            value_eur=value_eur,
        )

    transactions = user.all_transactions()

    return template(
        'account',
        username=user.get_username(),
        email=email,
        eur_balance=eur_balance,
        total_value=total_value,
        holdings=holdings,
        transactions=transactions,
        flash=flash,
        flash_type=flash_type,
    )

@route("/coin/<coin_id>")
def show_coin(coin_id):
    email = check_session()
    coin = Coin(coin_id)
    coin.make_graph()
    user = User(email)
    return template(
        "coin",
        coin_id    = coin_id,
        coin_name  = coin.get_coin_name(),
        coin_logo  = coin.get_coin_img_url(),
        price      = coin.get_todays_price(),
        change     = coin.get_change(),
        balance    = user.check_assets().get("EUR",-10),       # cash balance in USD,
        holdings   = user.check_assets().get(coin_id,-10),  # coins the user holds
        flash      = None,
        flash_type = None,
    )

@route("/coin/<coin_id>/trade", method="POST")
def trade_coin(coin_id):
    email = check_session()
    user = User(email)
    coin = Coin(coin_id)
    action = request.forms.get('action', 'buy')  # 'buy' or 'sell'

    try:
        amount = float(request.forms.get('amount', 0))
    except (ValueError, TypeError):
        amount = 0

    assets = user.check_assets()
    balance  = assets.get('EUR', 0)
    holdings = assets.get(coin_id, 0)
    price    = coin.get_todays_price()

    # --- validate amount ---
    if amount <= 0:
        flash, flash_type = "Please enter a valid amount.", "err"
    elif action == 'buy':
        cost = amount * price
        if cost > balance:
            flash, flash_type = "Insufficient balance for this purchase.", "err"
        else:
            # buy_sell expects % of EUR balance to spend
            pct = (cost / balance) * 100 if balance > 0 else 0
            ok = user.buy_sell(pct, 1, coin)
            flash      = f"Bought {round(amount, 6)} {coin.get_coin_name()}." if ok else "Trade failed."
            flash_type = "ok" if ok else "err"
    elif action == 'sell':
        if amount > holdings:
            flash, flash_type = "You don't hold enough coins to sell that amount.", "err"
        else:
            # buy_sell expects % of holdings to sell
            pct = (amount / holdings) * 100 if holdings > 0 else 0
            ok = user.buy_sell(pct, 0, coin)
            flash      = f"Sold {round(amount, 6)} {coin.get_coin_name()}." if ok else "Trade failed."
            flash_type = "ok" if ok else "err"
    else:
        flash, flash_type = "Unknown action.", "err"

    # re-fetch updated state for the re-render
    coin.make_graph()
    updated_assets = user.check_assets()
    return template(
        "coin",
        coin_id    = coin_id,
        coin_name  = coin.get_coin_name(),
        coin_logo  = coin.get_coin_img_url(),
        price      = price,
        change     = coin.get_change(),
        balance    = updated_assets.get("EUR", 0),
        holdings   = updated_assets.get(coin_id, 0),
        flash      = flash,
        flash_type = flash_type,
    )

#run(host='192.168.1.9', port=8080, debug=True)
run(host='127.0.0.1', port=8080, debug=True)
#192.168.1.15