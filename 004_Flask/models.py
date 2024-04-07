from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Article {self.id}>'


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)  # Email пользователя (уникальное поле)
#     username = db.Column(db.String(50), nullable=False)  # Имя пользователя
#     password_hash = db.Column(db.String(128), nullable=False)  # Хэш пароля пользователя
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Дата создания пользователя
#     login_count = db.Column(db.Integer, default=0)  # Количество входов пользователя
#     last_login = db.Column(db.DateTime)  # Дата последнего входа пользователя
#     is_admin = db.Column(db.Boolean, default=False)  # Признак администратора
#
#     first_name = db.Column(db.String(50))  # Имя пользователя
#     last_name = db.Column(db.String(50))  # Фамилия пользователя
#     date_of_birth = db.Column(db.Date)  # Дата рождения пользователя
#     avatar_url = db.Column(db.String(255))  # Ссылка на аватар пользователя
#     phone_number = db.Column(db.String(20))  # Номер телефона пользователя
#     is_active = db.Column(db.Boolean, default=True)  # Флаг активности аккаунта пользователя
#     is_verified = db.Column(db.Boolean, default=False)  # Флаг подтверждения аккаунта пользователя
#     country = db.Column(db.String(50))  # Страна проживания пользователя
#     city = db.Column(db.String(50))  # Город проживания пользователя
#     address = db.Column(db.String(255))  # Адрес проживания пользователя
#     registration_ip = db.Column(db.String(15))  # IP-адрес регистрации пользователя
#     last_ip = db.Column(db.String(15))  # Последний IP-адрес входа пользователя

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


