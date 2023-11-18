from flask import Blueprint, render_template, request, session, current_app
from app.hyldb.handler.user import UserHandler

test_bp = Blueprint('test', __name__, url_prefix="/test")


@test_bp.route('/')
def index():
    username = session.get('username')
    if username is None:
        return render_template("_base.html", username=username)
    return 'hyl, yyds!'


@test_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        body = request.json
        username = body.get('username')
        password = body.get('password')

        current_app.logger.info(f"login: user {username} identified by {password}")
        if username is None:
            return "Empty username", 400
        if password is None:
            return "Empty password", 400

        existing_user = User.get(filters={"username": username}, limitc=1)

        if existing_user is not None and existing_user.password == password:
            # Set the user token in the session upon successful login
            session['token'] = username
            return "Login successful!"
        else:
            return 'Authentication failed', 400

@test_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        body = request.json
        username = body.get('username')
        password = body.get('password')

        current_app.logger.info(f"register: user {username} identified by {password}")
        existing_user, ok = UserHandler.find_user(username)
        if not ok:
            return f"Internal error", 500
        if existing_user is not None:
            return f'Exsiting user {username}', 400

        UserHandler.add_user(username=username, password=password)

        return f'Register success'

@test_bp.route('/logout', methods=['GET'])
def logout():
    if 'Authorization' in session:
        current_app.logger.info(f"User {session.get('token')} logout")
        return "logout success"
    return "Empty token", 400
