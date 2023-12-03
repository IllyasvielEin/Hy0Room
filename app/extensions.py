from flask import Flask

from config import get_config, ConfigType
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

from app.utils.usermanager import UserManager
from app.utils.messgaefilter import MessageFilter


socketio = SocketIO()
online_user = UserManager()
db = SQLAlchemy()

message_filter = MessageFilter()
user_manager = UserManager()


def init_all(app: Flask):
    app.config.from_object(get_config(ConfigType.DevelopmentConfig))
    socketio.init_app(app)
    db.init_app(app)

    with app.app_context():
        # db.drop_all()
        db.create_all()


def start_socketio_run(app, **kwargs):
    socketio.run(app, **kwargs)


def init_db(app: Flask):
    from app.hyldb.handler.users import UserHandler, UserType
    from app.hyldb.models.permission import PermissionType
    from app.hyldb.handler.banwords import BanWordsHandler

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
                    id_number="0",
                    permission=PermissionType.ROOT,
                    state=UserType.NORMAL
                )
            except Exception as e:
                app.logger.error(f'{e}')
                return False
        all_words = BanWordsHandler.get_all()
        if all_words is None:
            exit(0)
        else:
            ban_word_db = [x.word for x in all_words]
            message_filter.add(
                ban_word_db
            )
            # app.logger.info(f"Load ban words: {ban_word_db}, words: {message_filter.get_words()}")

    return True
