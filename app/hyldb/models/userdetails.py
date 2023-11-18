from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class UserDetails(db.Model, GADBase):
    id = db.Column(db.Integer, primary_key=True)
    id_number = db.Column(db.String(20), unique=True, nullable=False)
    birthdate = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('details', uselist=False))

    def __repr__(self):
        return f"UserDetails(id={self.id}, id_card='{self.id_card}', birth_date='{self.birth_date}')"