import os
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from hw_models import db, User  # , Article
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HW_SQLALCHEMY_DATABASE_URI")
db.init_app(app)


# Создание таблиц внутри контекста приложения
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"An error occurred while creating database tables: {e}")


@app.route("/")
def base_():
    return render_template('hw_base.html', title="HW  Python course")


@app.route("/users")
def list_articles():
    users = User.query.order_by(User.date.desc()).all()
    return render_template("hw_users.html", users=users)


@app.route("/users/<int:id>/")
def articles_detail(id):
    user = User.query.get(id)
    return render_template("hw_users_detail.html", user=user)


@app.route("/create_user", methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password_hash = request.form["password_hash"]
        created_at = datetime.strptime(request.form["created_at"], "%Y-%m-%dT%H:%M")
        login_count = int(request.form["login_count"])
        last_login = datetime.strptime(request.form["last_login"], "%Y-%m-%dT%H:%M")
        is_admin = request.form["is_admin"]

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        date_of_birth = datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d")
        avatar_url = request.form["avatar_url"]
        phone_number = request.form["phone_number"]
        is_active = request.form["is_active"]
        is_verified = request.form["is_verified"]
        country = request.form["country"]
        city = request.form["city"]
        address = request.form["address"]
        registration_ip = request.form["registration_ip"]
        last_ip = request.form["last_ip"]

        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
            created_at=created_at,
            login_count=login_count,
            last_login=last_login,
            is_admin=is_admin,

            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            avatar_url=avatar_url,
            phone_number=phone_number,
            is_active=is_active,
            is_verified=is_verified,
            country=country,
            city=city,
            address=address,
            registration_ip=registration_ip,
            last_ip=last_ip
        )
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        except Exception as exc:
            return f"При сохранении записи в базу данных произошла ошибка: {exc}"
    else:
        return render_template("create_user.html")


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
