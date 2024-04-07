import os
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from models import db, Article, User
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)


# # Создание таблиц внутри контекста приложения
# with app.app_context():
#     try:
#         db.create_all()
#     except Exception as e:
#         print(f"An error occurred while creating database tables: {e}")


@app.route("/")
def base_():
    return render_template('base.html', title="Python course")


@app.route("/create_article", methods=["POST", "GET"])
def create_article():
    if request.method == "POST":
        title = request.form["title"]
        intro = request.form["intro"]
        text = request.form["text"]

        article = Article(
            title=title,
            intro=intro,
            text=text
        )
        try:
            db.session.add(article)
            db.session.commit()
            return redirect("/")
        except Exception as exc:
            return f"ПРи збереженні запису у базу даних виникла помилка: {exc}"
    else:
        return render_template("create_article.html")


@app.route("/articles")
def list_articles():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("articles.html", articles=articles)


@app.route("/articles/<int:id>/")
def articles_detail(id):
    article = Article.query.get(id)
    return render_template("articles_detail.html", article=article)


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
