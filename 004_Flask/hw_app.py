import os
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from hw_models import db, User  # , Article
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("HW_SQLALCHEMY_DATABASE_URI")
db.init_app(app)


# # Создание таблиц внутри контекста приложения
# with app.app_context():
#     try:
#         db.create_all()
#     except Exception as e:
#         print(f"An error occurred while creating database tables: {e}")


@app.route("/")
def hw_base_():
    return render_template('hw_base.html', title="HW  Python course")


@app.route("/hw_users")
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("hw_users.html", users=users)


@app.route("/hw_users/<int:id>/")
def users_detail(id):
    user = User.query.get(id)
    return render_template("hw_users_detail.html", user=user)


@app.route("/hw_create_user", methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password_hash = request.form["password_hash"]
        # created_at = datetime.strtime(request.form["created_at"], "%Y-%m-%dT%H:%M")

        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
            # created_at=created_at

        )
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/hw_users")
        except Exception as exc:
            return f"При сохранении записи в базу данных произошла ошибка: {exc}"
    else:
        return render_template("hw_create_user.html")


@app.route("/hw_users/<int:id>/delete")
def user_delete(id):
    user = User.query.get_or_404(id)

    try:
        db.session.delete(user)
        db.session.commit()
        return redirect("/hw_users")
    except Exception as exc:
        return f"При удалении пользователя произошла ошибка: {exc}"
# @app.route("/hw_users/<int:id>/delete", methods=["POST"])
# def user_delete(id):
#     if request.method == "POST":
#         user = User.query.get_or_404(id)
#
#         try:
#             db.session.delete(user)
#             db.session.commit()
#             return redirect("/hw_users")
#         except Exception as exc:
#             return f"При удалении пользователя произошла ошибка: {exc}"


@app.route("/hw_users/<int:id>/update", methods=["POST", "GET"])
def user_update(id):
    # user = User.query.get(id)
    user = User.query.get_or_404(id)

    if request.method == "POST":
        user.email = request.form["email"]
        user.username = request.form["username"]
        user.password_hash = request.form["password_hash"]

        try:
            db.session.commit()
            return redirect("/hw_users")
        except Exception as exc:
            return f"Про обновлении записи произошла ошибка: {exc}"
    else:
        return render_template("hw_user_update.html", user=user)


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
