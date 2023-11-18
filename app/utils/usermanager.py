from flask import current_app


class UserManager:
    def __init__(self, max_user=65535):
        self._user = set()
        self._max_user = max_user

    def add_user(self, username):
        if len(self._user) + 1 >= self._max_user:
            return False
        self._user.add(username)
        return True

    def remove_user(self, username):
        try:
            self._user.remove(username)
        except KeyError as e:
            current_app.logger.warning(f"Remove a empty user: {username}")
