from flask import Flask, render_template

app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route("/")
def main():
    return render_template("welcome_NK.html")


@app.route("/birthday")
def birthday():
    return render_template("lk_birthday.html")


@app.route("/Full_Name")
def full_name():
    return render_template("lk_Full_Name.html")


@app.route("/hobby")
def hobby():
    return render_template("lk_hobby.html")


if __name__ == '__main__':
    app.run(host="127.1.1.1", port=1234, debug=True)