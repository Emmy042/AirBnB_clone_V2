#!/usr/bin/python3
"""Flask app to list states and their cities"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)

@app.teardown_appcontext
def teardown_db(exception):
    """Close storage session after request"""
    storage.close()

@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display all states and their cities"""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template('8-cities_by_states.html', states=states)

if __name__ == '__main__':
    app.run(debug=True)
