from app.extensions import db
from datetime import datetime
from app.hyldb.models.basehandle.mixin import GADBase


class BanWords(db.Model, GADBase):
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    word = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"ForbiddenWord(id={self.id}, word='{self.word}')"
