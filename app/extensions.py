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


def init_db(app: Flask):
    from app.hyldb.handler.users import UserHandler
    from app.hyldb.models.permission import PermissionType
    with app.app_context():
        res, ok = UserHandler.get_user_by_id(1)
        if not ok:
            print("Error while db init")
            return False

        if res is None:
            try:
                UserHandler.add_user(
                    user_id=1,
                    username="admin",
                    password="admin",
                    student_id="0",
                    real_name="admin",
                    permission=PermissionType.ROOT
                )
            except Exception as e:
                app.logger.error(f'{e}')
                return False
    return True
