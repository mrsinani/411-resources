from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @classmethod
    def create_user(cls, username, password):
        if cls.query.filter_by(username=username).first():
            raise ValueError("User already exists")
        user = cls(username, password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def check_password(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if not user:
            return False
        return check_password_hash(user.password_hash, password)

    @classmethod
    def delete_user(cls, username):
        user = cls.query.filter_by(username=username).first()
        if not user:
            raise ValueError("User does not exist")
        db.session.delete(user)
        db.session.commit()
