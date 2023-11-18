from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class BanWords(db.Model, GADBase):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"ForbiddenWord(id={self.id}, word='{self.word}')"