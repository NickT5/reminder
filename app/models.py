"""
To create/delete the database tables:
python
> from app import db
> db.create_all()
> db.drop_all()
> exit()
"""
from app import db, bcrypt
from flask_login import UserMixin


class Task(db.Model):
    """
    Task database table.
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    deadline = db.Column(db.String(50), nullable=True)
    date_created = db.Column(db.DateTime, nullable=False)
    is_done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.text}')"


class User(db.Model, UserMixin):
    """
    User database table.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User({self.username}, {self.email}, role={self.role})"

