from flask import current_app

from app.hyldb.handler.users import UserHandler
from app.hyldb.models.permission import Permission, PermissionType


class PermissionHandler:

    @staticmethod
    def set_permission(user: int|str, perm: PermissionType):
        if user is None:
            current_app.logger.warning("user is None")
            return

        user_id = user
        if isinstance(user, str):
            user_id = UserHandler.get_user_by_name(user)[0].id

        Permission.update(oid=user_id, kv={
            'authority_type': perm
        })
