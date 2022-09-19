#!/usr/bin/python3
"""states"""

from api.v1.views import app_views
import json
from models import storage
from flask import jsonify, make_response, request, abort
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def all(state_id=None):
    """list all states"""
    if state_id is not None:
        if not storage.get(State, state_id):
            abort(404)
        elem = storage.get(State, state_id).to_dict()
        return jsonify(elem)
    else:
        listobj = []
        for obj in storage.all(State).values():
            listobj.append(obj.to_dict())
        return jsonify(listobj)


@app_views.route('states/<state_id>', methods=['DELETE'], strict_slashes=False)
def dell(state_id):
    """delete"""
    elem = storage.get(State, state_id)
    if not elem:
        abort(404)
    storage.delete(elem)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def posting():
    """post"""
    req = request.json
    if not req:
        abort(400, description="Not a JSON")
    if 'name' not in req:
        abort(400, description="Missing name")
    info = State(**req)
    info.save()
    return make_response(jsonify(info.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def putting(state_id):
    """put"""
    req = request.json
    if not req:
        abort(400, description="Not a JSON")
    if not storage.get(State, state_id):
        abort(404)
    badkeys = ['id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in badkeys:
            elem = storage.get(State, state_id)
            setattr(elem, key, value)
    storage.save()
    return make_response(jsonify(elem.to_dict()), 200)
