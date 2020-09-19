# services/users/project/api/users/models.py


import os
from datetime import datetime, timezone, timedelta

import jwt
from flask import current_app
from sqlalchemy.sql import func

from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username="", email="", password=""):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get("BCRYPT_LOG_ROUNDS")
        ).decode()

    # https://realpython.com/token-based-authentication-with-flask/
    def encode_token(self, user_id, token_type):
        if token_type == "access":
            seconds = current_app.config.get("ACCESS_TOKEN_EXPIRATION")
        else:
            seconds = current_app.config.get("REFRESH_TOKEN_EXPIRATION")

        payload = {
            # https://docs.python.org/3/library/datetime.html
            "exp": datetime.now(timezone.utc) + timedelta(seconds=seconds),
            "iat": datetime.now(timezone.utc),
            "sub": user_id,
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            "active": self.active,
            "created_date": self.created_date.isoformat()
        }        

    # https://realpython.com/token-based-authentication-with-flask/
    # We have used a static method since it does not relate to the class’s instance.
    @staticmethod
    def decode_token(token):
        payload = jwt.decode(token, current_app.config.get("SECRET_KEY"))
        return payload["sub"]


if os.getenv("FLASK_ENV") == "development":
    from project import admin
    from project.api.users.admin import UsersAdminView

    admin.add_view(UsersAdminView(User, db.session))
