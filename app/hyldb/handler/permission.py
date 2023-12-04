from flask import current_app

from app.hyldb.handler.users import UserHandler
from app.hyldb.models.permission import Permission, PermissionType


class PermissionHandler:

    @staticmethod
    def set_permission(user: int | str, perm: PermissionType):
        if user is None:
            current_app.logger.warning("user is None")
            return

        user_id = user
        if isinstance(user, str):
            user_id = UserHandler.get_user_by_name(user)[0].id

        Permission.update(
            oid=user_id, kv={
                'authority_type': perm
            })

    @staticmethod
    def check_is(user_id, permission: PermissionType):
        res = Permission.get(
            filters={
                'user_id': user_id
            },
            limitc=1
        )

        if res is not None:
            return res.permession_type == permission
        else:
            current_app.logger.error(f"Empty search, please check output")

        return False

    @staticmethod
    def is_root(user_id: int):
        return PermissionHandler.check_is(user_id, PermissionType.ROOT)

    @staticmethod
    def is_admin(user_id: int):
        return (PermissionHandler.check_is(user_id, PermissionType.ROOT)
                or PermissionHandler.check_is(user_id, PermissionType.ADMIN))

    @staticmethod
    def a_is_higher_permission(user_a_id, user_b_id):
        res1 = Permission.get(
            filters={
                'user_id': user_a_id
            },
            limitc=1
        )

        res2 = Permission.get(
            filters={
                'user_id': user_b_id
            },
            limitc=1
        )

        if res1 is not None and res2 is not None:
            return res1.permission_type.value < res2.permission_type.value

        raise ValueError("Search error")