from typing import Dict, List

from flask import current_app

from app.hyldb.models.permission import PermissionType, Permission
from app.hyldb.models.users import Users
from app.hyldb.models.userdetails import UserDetails


class UserHandler:

    @staticmethod
    def get_user_by_name(username: str):
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
    def get_user_by_id(user_id: int):
        ok = True
        try:
            res = Users.get_one_by_id(oid=user_id)
        except Exception as e:
            current_app.logger.error(f"{e}")
            ok = False
            res = None
        return res, ok

    @staticmethod
    def add_user(username: str,
                 password: str,
                 student_id: str,
                 real_name: str,
                 user_id: int = None,
                 permission: PermissionType = PermissionType.USER):
        ok = True
        try:
            if user_id is not None:
                res = Users.add(id=user_id, username=username, password=password)
            else:
                res = Users.add(username=username, password=password)
        except Exception as e:
            current_app.logger.error(f'{e}')
            ok = False
            res = None

        if ok:
            try:
                UserDetails.add(user_id=res.id, student_id=student_id, real_name=real_name)
                Permission.add(
                    user_id=res.id,
                    permission_type=permission
                )
            except Exception as e:
                Users.delete(res)
                ok = False
                res = None

        return res, ok

    @staticmethod
    def get_channels_info(username: str):
        user, ok = UserHandler.get_user_by_name(username)
        res = None
        if ok and user is not None:
            res = [{
                "name": x.name,
                "created": x.created_at
            } for x in user.channels]
        return res

    @staticmethod
    def update_user_info(user_id: int, kv: Dict):
        ok = Users.update(oid=user_id, kv=kv)
        if ok:
            tmp_filter = {
                'user_id': user_id
            }
            ok = UserDetails.update(find_filter=tmp_filter, kv=kv)
        return ok

    @staticmethod
    def get_all():
        try:
            res = Users.get()
        except Exception as e:
            current_app.logger.error(f"Error {e} occur while getting all user")
            res = None
        return res

    @staticmethod
    def get_all_id_in_list(id_list: List[int]):
        res = []
        try:
            for each_id in id_list:
                res.append(Users.get(filters={'id': each_id}, limitc=1))
        except Exception as e:
            res = None
        return res
