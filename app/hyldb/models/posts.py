from enum import Enum
from datetime import datetime
from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class PostState(Enum):
    NORMAL = 1
    HIDDEN = 2
    DELETE = 3
    BEFOREAUDIT = 3
    FORBIDDEN = 4

class Posts(db.Model, GADBase):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    last_edited_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow(), nullable=False)

    state = db.Column(db.Enum(PostState), default=PostState.NORMAL, nullable=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    comments = db.relationship('Posts', backref=db.backref('parent', remote_side=[id]))
    creator = db.relationship('Users', backref=db.backref('posts'))

    def __repr__(self):
        return '<Post %r>' % self.id
