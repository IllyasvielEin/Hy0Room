from app.extensions import db
from datetime import datetime
from app.hyldb.models.basehandle.mixin import GADBase


class Channels(db.Model, GADBase):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # users = db.relationship('User', secondary='user_channel', backref='channels')

    def __repr__(self):
        return f"ChatRoom(id={self.id}, name='{self.name}', description='{self.description}')"

