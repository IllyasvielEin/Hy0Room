from app.extensions import db
from datetime import datetime
from app.hyldb.models.basehandle.mixin import GADBase


class Channels(db.Model, GADBase):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    # users = db.relationship('User', secondary='user_channel', backref='channels')

    def __repr__(self):
        return f"ChatRoom(id={self.id}, name='{self.name}', description='{self.description}')"


user_channel = db.Table(
    'user_channel',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True)
)