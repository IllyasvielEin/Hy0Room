from datetime import datetime
from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class Users(db.Model, GADBase):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    crated_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    channels_creator = db.relationship('Channels', backref=db.backref('creator'))

    def __repr__(self):
        return '<User %r>' % self.username

    def __eq__(self, other):
        return isinstance(other, Users) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
