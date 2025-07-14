#!/usr/bin/python3
"""Flask app for /states_list route"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Remove SQLAlchemy session after each request"""
    storage.close()

@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display HTML page with states listed"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda s: s.name)
    return render_template('7-states_list.html', states=states)

if __name__ == '__main__':
    app.run(debug=True)
