import os
from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from models import db, Article
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
            return redirect("/articles  ")
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


@app.route("/articles/<int:id>/delete")
def articles_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect("/articles")
    except Exception as exc:
        return f"При удалении окна ощибка: {exc}"


@app.route("/articles/<int:id>/update", methods=["POST", "GET"])
def articles_update(id):
    article = Article.query.get(id)

    if request.method == "POST":
        article.title = request.form["title"]
        article.intro = request.form["intro"]
        article.text = request.form["text"]

        try:
            db.session.commit()
            return redirect("/articles")
        except Exception as exc:
            return f"Про обновлении записи произошла ошибка: {exc}"
    else:
        return render_template("article_update.html", article=article)


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))
