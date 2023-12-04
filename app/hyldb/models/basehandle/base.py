from typing import Dict

from flask import current_app
from sqlalchemy import and_

from app.extensions import db


class CreateBase:
    @classmethod
    def add(cls, **kwargs):
        try:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f'{e}')
            db.session.rollback()
            instance = None
        return instance


class ReadBase:
    @classmethod
    def get(cls, filters: Dict | None = None, filter_condition=None, sorter: str | None = None, limitc=None):
        query = cls.query

        if filters:
            query = query.filter_by(**filters)
        elif filter_condition:
            query = query.filter(filter_condition)

        if sorter:
            if sorter.startswith("+"):
                column = sorter[1:]
                query = query.order_by(getattr(cls, column))
            elif sorter.startswith("-"):
                column = sorter[1:]
                query = query.order_by(getattr(cls, column).desc())
            else:
                query = query.order_by(sorter)

        res = None
        if limitc is not None:
            if limitc == 1:
                res = query.first()  # 使用 first() 获取单个结果
            elif limitc:
                query = query.limit(limitc)
                res = query.all()
        else:
            res = query.all()

        return res

    @classmethod
    def get_one_by_id(cls, oid: int):
        obj = cls.query.get(oid)
        return obj if obj else None


class DeleteBase:

    @classmethod
    def delete(cls, oid=None, filters=None):
        if oid:
            query = cls.query.filter(cls.id == oid)

        elif filters:
            query = cls.query.filter(
                and_(*[getattr(cls, k) == v for k, v in filters.items()])
            )
        else:
            raise ValueError("Must provide either an object ID or a filter.")

        query.delete(synchronize_session='fetch')
        db.session.commit()


class UpdateBase:
    @classmethod
    def update(cls, oid=None, find_filter: Dict | None = None, kv=None):
        if (oid is None and find_filter is None) or kv is None:
            current_app.logger.error(f"Empty oid or kv: {oid}, {kv}")
            return False

        if oid is not None:
            instance = cls.query.get(oid)
        elif find_filter is not None:
            instance = cls.query.filter_by(**find_filter).first()
        if instance:
            try:
                for key, value in kv.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)

                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return False
        return True
