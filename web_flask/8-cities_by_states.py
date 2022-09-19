#!/usr/bin/python3
"""task 7"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_app(self):
    """bye"""
    storage.close()


@app.route("/cities_by_states", strict_slashes=False)
def cities_list():
    """list cities"""
    states = storage.all(State).values()
    states = sorted(statesList, key=lambda k: k.name)
    return render_template("8-cities_by_states.html", states)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
