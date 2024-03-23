from flask import Flask, render_template,  redirect, url_for

# WSGI Application
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/welcome')
def welcome():
    return '''This is the home page of Flask Application. Welcome! <br>
            <a href="/birthday">Birthday</a><br>
            <a href="/full_name">Full Name</a><br>
            <a href="/hobby">Hobby</a>'''


@app.route('/birthday')
def birthday():
    return '''<a href="/welcome">Welcome</a><br>
            I was born on July 10, 2010!<br>
            <a href="/full_name">Full Name</a><br>
            <a href="/hobby">Hobby</a><br>'''


@app.route('/full_name')
def full_name():
    return '''<a href="/welcome">Welcome</a><br>
            <a href="/birthday">Birthday</a><br>
            My name is Nikita Leonidovich Kadantsev.<br>
            <a href="/hobby">Hobby</a><br>'''


@app.route('/hobby')
def hobby():
    my_hobby = '''<a href="/welcome">Welcome</a><br>
                <a href="/birthday">Birthday</a><br>
                <a href="/full_name">Full Name</a><br>
                My Hobbies:
                <br>- Playing computer games
                <br>- Chess
                <br>- Programming (Python)
                <br>- Karate
                <br>- Swimming
                <br>- Cycling
                <br>- Family road trips by car<br>'''
    return my_hobby


# @app.route('/')
# def index():
#     return render_template('index.html')
@app.route('/')
def index():
    return redirect(url_for('welcome'))

# redirect: Эта функция используется для перенаправления пользователя на другую страницу.
#           Она принимает URL-адрес в качестве аргумента и возвращает ответ перенаправления клиенту.
#
# url_for: Эта функция используется для создания URL-адресов для функций представления в вашем приложении Flask.
#           Она принимает имя функции представления в качестве аргумента и возвращает URL-адрес для этой функции.


if __name__ == '__main__':
    app.run(host="127.1.1.1", port=1234, debug=True)
