from flask import Flask

app = Flask(__name__)

@app.route("/", strict_slashes=False)
def hello():
    return "<p>Hello HBNB</p>"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    return f"C {text.replace('_', ' ')}"

@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def Python_text(text='is cool'):
    return f"Python {text.replace('_', ' ')}"


if __name__ == '__main__':
    app.run(debug=True)
