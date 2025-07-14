#!/usr/bin/python3
"""Flask app to display states and cities"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes SQLAlchemy session after each request"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states_list():
    """Displays a list of all States sorted by name"""
    states = sorted(storage.all(State).values(), key=lambda s: s.name)
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """Displays cities of a State if found, else 'Not found!'"""
    states = storage.all(State).values()
    for state in states:
        if state.id == id:
            cities = state.cities if hasattr(state, 'cities') else state.get_cities()
            cities = sorted(cities, key=lambda c: c.name)
            return render_template('9-states.html', state=state, cities=cities)
    return render_template('9-states.html', state=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
