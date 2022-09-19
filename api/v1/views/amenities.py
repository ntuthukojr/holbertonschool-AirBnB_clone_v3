#!/usr/bin/python3
"""amenities"""

from api.v1.views import app_views
import json
from models import storage
from flask import jsonify, make_response, request, abort
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def listamen(amenity_id):
    """list amenity"""
    if not storage.get(Amenity, amenity_id):
        abort(404)
    elem = storage.get(Amenity, amenity_id).to_dict()
    return jsonify(elem)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenshow():
        listobj = []
        for obj in storage.all(Amenity).values():
            listobj.append(obj.to_dict())
        return jsonify(listobj)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delamen(amenity_id):
    """delete"""
    elem = storage.get(Amenity, amenity_id)
    if not elem:
        abort(404)
    storage.delete(elem)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def postamen():
    """post"""
    req = request.get_json()
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in req:
        abort(400, description="Missing name")
    info = Amenity(**req)
    info.save()
    return make_response(jsonify(info.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def putamen(amenity_id):
    """put"""
    req = request.get_json()
    if not req:
        abort(400, description="Not a JSON")
    if not storage.get(Amenity, amenity_id):
        abort(404)
    badkeys = ['id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in badkeys:
            elem = storage.get(Amenity, amenity_id)
            setattr(elem, key, value)
    storage.save()
    return make_response(jsonify(elem.to_dict()), 200)
