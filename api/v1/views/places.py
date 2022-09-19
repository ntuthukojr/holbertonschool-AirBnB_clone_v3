#!/usr/bin/python3

"""place"""

from api.v1.views import app_views
import json
from models import storage
from flask import jsonify, make_response, request, abort
from models.city import City
from models.state import State
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_all(city_id):
    """list all places in city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    listobj = []
    for obj in city.places:
        listobj.append(obj.to_dict())
    return jsonify(listobj)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_get(place_id):
    """place info"""
    elem = storage.get(Place, place_id)
    if not elem:
        abort(404)
    return jsonify(elem.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_del(place_id):
    """delete"""
    elem = storage.get(Place, place_id)
    if not elem:
        abort(404)
    storage.delete(elem)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """post"""
    req = request.get_json()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not req:
        abort(400, description="Not a JSON")
    if 'user_id' not in req:
        abort(400, description="Missing user_id")
    if not storage.get(User, req['user_id']):
        abort(404)
    if 'name' not in req:
        abort(400, description="Missing name")
    req["city_id"] = city_id
    info = Place(**req)
    info.save()
    return make_response(jsonify(info.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """put"""
    req = request.json
    if not req:
        abort(400, description="Not a JSON")
    if not storage.get(Place, place_id):
        abort(404)
    badkeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in badkeys:
            elem = storage.get(Place, place_id)
            setattr(elem, key, value)
    storage.save()
    return make_response(jsonify(elem.to_dict()), 200)
