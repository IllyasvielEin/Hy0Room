from app.extensions import db
from app.hyldb.models.basehandle.mixin import GADBase


class UserDetails(db.Model, GADBase):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    real_name = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.String(10), unique=True, nullable=False)

    user = db.relationship('Users', backref=db.backref('details', uselist=False))

    def __repr__(self):
        return f"UserDetails(id={self.id}, real_name={self.real_name}, student_id='{self.student_id}'')"
