from enum import Enum
from datetime import datetime
from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class PermissionType(Enum):
    ROOT = 0
    ADMIN = 1
    USER = 2

class Permission(db.Model, GADBase):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    crated_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    permission_type = db.Column(db.Enum(PermissionType), default=PermissionType.USER, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id}: {self.authority_type}>'
