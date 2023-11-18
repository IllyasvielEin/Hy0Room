from typing import Dict
from app.extensions import db


class AddBase:
    @classmethod
    def add(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance


class GetBase:
    @classmethod
    def get(cls, filters: Dict | None = None, sorter: str | None = None, limitc=None):
        query = cls.query

        if filters:
            query = query.filter_by(**filters)

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

class DelBase:

    @classmethod
    def delete(cls, obj=None, oid=None):
        ok = True
        try:
            if obj:
                cls.query.delete(obj)
            elif oid:
                obj = cls.query.get(oid)
                if obj:
                    cls.query.delete(obj)
            db.session.commit()
        except Exception as e:
            ok = False
        return ok


