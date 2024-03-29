import os
from flask import Flask, render_template
from dotenv import load_dotenv
from enums import MAX_SCORE, NAME, students

load_dotenv()
app = Flask(__name__)


# app = Flask(__name__, template_folder='template', static_folder='static')
@app.route("/")
def index_():
    # return render_template('index.html')
    return render_template('base.html', title="Python course")


# @app.route("/base")
# def base_():
#     return render_template('base.html', title="Python course")


@app.route("/context")
def context_():
    context_dict = {
        "title": "Python Course",
        "name": NAME,
        "max_score": MAX_SCORE,
        "students": students
    }
    return render_template('context.html', **context_dict)

@app.route("/test")
def text_():
    text_dict = {
        "title": "Python Course - Page Test",
        "str_title": "This is a test page",
        "str_window":'Цей шаблон я буду використовувати в проекті замість розділу "About".'
    }
    return render_template('test.html', **text_dict)


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"))

    # {# Это кусок кода, который стал временно не нужен, но удалять жалко
    #     { % for user in users %}
    # ...
    # { % endfor %}
    # #}
