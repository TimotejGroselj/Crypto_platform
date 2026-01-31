from bottle import route, run, template, static_file, request,redirect


# 1. serve CSS
@route('/static/<filename>')
def static_files(filename):
    return static_file(filename, root='./static')

# 2. show login page
@route('/')
def show_login():
    return template('login')

@route('/login', method='POST')
def login_logic():
    username = request.forms.get('username')
    password = request.forms.get('password')

    if username == 'admin' and password == '1234':
        return "<h1>Success!</h1>"
    else:
        return template('incorrect')


@route('/dashboard')
def dashboard():
    return "<h1>You are logged in</h1>"

# 3. start server
run(host='localhost', port=8080, debug=True)