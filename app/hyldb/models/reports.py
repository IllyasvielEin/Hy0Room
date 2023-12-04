from enum import Enum
from datetime import datetime
from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class ReportState(Enum):
    JUDGING = 1
    GUILTY = 2
    NOTGUILTY = 3

class ReportType(Enum):
    CHANNEL = 1
    CHANNEL_CHAT = 2
    POST = 3
    POST_COMMENT = 4
    USER_NAME = 5
    USER_ACTION = 6

class Reports(db.Model, GADBase):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    last_edited_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)

    state = db.Column(db.Enum(ReportState), default=ReportState.JUDGING, nullable=False)
    content = db.Column(db.Text, nullable=False)
    content_id = db.Column(db.Integer, nullable=False)
    content_type = db.Column(db.Enum(ReportType), nullable=False)
    accuser_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accused_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    accuser = db.relationship('Users', foreign_keys=[accuser_id])
    accused = db.relationship('Users', foreign_keys=[accused_id])

    def __repr__(self):
        return '<Post %r>' % self.id
