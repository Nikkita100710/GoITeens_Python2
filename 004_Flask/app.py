import os
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from models import db, Article, User

load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
db.init_app(app)


# Создание таблиц внутри контекста приложения
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"An error occurred while creating database tables: {e}")


@app.route("/")
def base_():
    return render_template('base.html', title="Python course")


@app.route("/create-article", methods=["POST", "GET"])
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


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
