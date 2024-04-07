from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email пользователя (уникальное поле)
    username = db.Column(db.String(50), nullable=False)  # Имя пользователя
    password_hash = db.Column(db.String(128), nullable=False)  # Хэш пароля пользователя
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата создания пользователя

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


