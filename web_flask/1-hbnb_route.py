from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    return "<p>Hello HBNB</p>"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"

if __name__ == '__main__':
    app.run(debug=True)
