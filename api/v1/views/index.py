#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
import json
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    """stat"""
    return ({"status": "OK"})


@app_views.route('stats')
def count():
    """counter"""
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    count = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
     }
    return (count)
