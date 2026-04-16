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
        market_change = show_market(coin, 1)
        box_el[coin.get_coin_id()] = dict(logo = coin.get_coin_img_url(), name = coin.get_coin_name(), price = coin.get_todays_price(),change = coin.get_change(), market_change = market_change)
    transactions = user.all_transactions()


    return template("dashboard", box_el = box_el, transactions = transactions)

@route("/dashboard", method='POST')
def dashboard_logic():
    check_session()
    action = request.forms.get('type')
    coin_id = request.forms.get('coin')
    amount = float(request.forms.get('amount'))
    user = User(sessions[request.cookies.get('session_id')])
    user.buy_sell(amount, action, Coin(coin_id))
    redirect("/dashboard")

    



   
@route("/logout")
def logout():
    session_id = request.cookies.get('session_id')
    if session_id in sessions:
        del sessions[session_id]
    response.delete_cookie('session_id')
    for pic in os.listdir("temp"):
        os.remove(f"temp/{pic}")
    redirect("/")
    
@route("/coin/<coin_id>")
def show_coin(coin_id):
    check_session()
    coin = Coin(coin_id)
    os.makedirs("temp", exist_ok=True)
    coin.make_graph()
    return template("coin", coin_id=coin_id)

#run(host='192.168.1.9', port=8080, debug=True)
run(host='127.0.0.1', port=8080, debug=True)
#192.168.1.15