from enum import Enum

from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase

class MessageState(Enum):
    NORMAL = 1
    WITHDRAWN = 2
    VIOLATION = 3

class Messages(db.Model, GADBase):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    send_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    state = db.Column(db.Enum(MessageState), default=MessageState.NORMAL, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    user = db.relationship('Users', backref='messages', foreign_keys=[user_id])
    channel = db.relationship('Channels', backref='messages')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'channel_id': self.channel_id,
            'content': self.content,
            'send_at': self.send_at,
            'state': self.state.value
        }

    def __repr__(self):
        return f"{self.user.username}<{self.user_id}> said {self.content} in room{self.channel_id} at {self.send_at}"
