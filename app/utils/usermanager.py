from typing import List, Dict, Set

from flask import current_app


class UserManager:
    def __init__(self, max_user=65535):
        self._user_channel_map: Dict[str: int] = dict()
        self._channel_user_map: Dict[int: Set] = dict()
        self._max_user = max_user

    def add_user(self, channel_id, user):
        current_app.logger.info(f"{channel_id} add user {user}")
        if len(self._user_channel_map) + 1 >= self._max_user:
            return False
        if channel_id not in self._channel_user_map:
            self._channel_user_map[channel_id] = set()
        self.remove_user(user)
        self._user_channel_map[user] = channel_id
        self._channel_user_map[channel_id].add(user)
        return True

    def remove_user(self, user):
        if user in self._user_channel_map:
            user_in_channel = self._user_channel_map[user]
            if user in self._channel_user_map[user_in_channel]:
                self._channel_user_map[user_in_channel].remove(user)
                current_app.logger.info(f"user {user} leave {user_in_channel}")
            self._user_channel_map.pop(user)

    def get_channel_user(self, channel_id) -> List[str]:
        return [user for user in self._channel_user_map[channel_id]]
