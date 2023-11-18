from flask import current_app

from app.hyldb.models.users import Users

class UserHandler:

    @staticmethod
    def find_user(username: str):
        tmp_filter = {
            "username": username
        }
        ok = True
        try:
            res = Users.get(filters=tmp_filter, limitc=1)
        except Exception as e:
            current_app.logger.error(f"{e}")
            ok = False
            res = None
        return res, ok

    @staticmethod
    def add_user(username: str, password: str):
        ok = True
        try:
            res = Users.add(username=username, password=password)
        except Exception as e:
            current_app.logger.error(f'{e}')
            ok = False
            res = None
        return res, ok

    @staticmethod
    def get_channels_info(username: str):
        user, ok = UserHandler.find_user(username)
        res = None
        if ok and user is not None:
            res = [{
                "name": x.name,
                "created": x.created_at
            } for x in user.channels]
        return res
