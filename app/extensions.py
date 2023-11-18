from flask import Flask
from config import get_config, ConfigType
from flask_socketio import SocketIO
from app.utils.usermanager import UserManager
from flask_sqlalchemy import SQLAlchemy

socketio = SocketIO()
online_user = UserManager()
db = SQLAlchemy()

def init_all(app: Flask):
    app.config.from_object(get_config(ConfigType.DevelopmentConfig))
    socketio.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

def start_socketio_run(app, **kwargs):
    socketio.run(app, **kwargs)
