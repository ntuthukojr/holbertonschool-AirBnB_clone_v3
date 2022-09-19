#!/usr/bin/python3
"""city"""

from api.v1.views import app_views
import json
from models import storage
from flask import jsonify, make_response, request, abort
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_all(state_id):
    """list all states"""
    if not storage.get(State, state_id):
        abort(404)
    elem = storage.get(State, state_id)
    listobj = []
    for obj in elem.cities:
        listobj.append(obj.to_dict())
    return jsonify(listobj)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def cit_getter(city_id):
    elem = storage.get(City, city_id)
    if not elem:
        abort(404)
    return jsonify(elem.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_del(city_id):
    """delete"""
    elem = storage.get(City, city_id)
    if not elem:
        abort(404)
    storage.delete(elem)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """post"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    req = request.get_json()
    info = City(**req)
    info.state_id = state.id
    info.save()
    return make_response(jsonify(info.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """put"""
    req = request.json
    if not req:
        abort(400, description="Not a JSON")
    if not storage.get(City, city_id):
        abort(404)
    badkeys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in badkeys:
            elem = storage.get(City, city_id)
            setattr(elem, key, value)
    storage.save()
    return make_response(jsonify(elem.to_dict()), 200)
