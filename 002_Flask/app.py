
from flask import Flask

app = Flask(__name__)


@app.route('/')
def main():
    return "This is a main page NK"


print(__name__)  # Expected to receive "main"
app.run(host="127.1.1.1", port=1234, debug=True)
