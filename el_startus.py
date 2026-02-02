from bottle import route, run, template, static_file, request,redirect
from el_login import *
from class_user import *


@route('/static/<filename>')
def static_files(filename):
    """Ovaj za css fileje"""
    return static_file(filename, root='./static')

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
    if email == 'bon@gmail.com':
        return template('login', error='This email does not exist!', email=email, password=None)
    #if not l.is_user(email):
    #    return template('login',error='This email does not exist!',email=email,password=None)
    #if not l.valid_login(email, password):
    #    return template('login', error='Incorrect password!', email=email, password=None)
    user = 'GOVEDO JEDNO'
    #user = User(email).get_username()
    return redirect(f"/greet?name={user}")


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

    l = Login()

    if not l.valid_email(email):
        return template('register',error ='Please insert a valid email!',username=username,email=None,password=password)
    #if l.is_user(email):
    #    return template('register',error ='User with that email already exists!',username=username,email=email,password=password)
    valid = l.valid_password(password)
    if valid is not None:
        return template('register',error="Chose a stronger password!",username=username,email=email,password=None)
    if password != confirm_password:
        return template('register',error ='Passwords do not match!',username=username,email=email,password=password)
    #l.create_user(username,email,password)
    return template("login",error=None,email=email,password=None)


@route('/greet')
def dashboard():
    name = request.query.get('name')
    return template("success",name=name)

@route('/dashboard')
def show_dashboard():
    return template("dashboard")

@route("/dashboard", method='POST')
def dashboard_logic():
    return None

run(host='localhost', port=8080, debug=True)