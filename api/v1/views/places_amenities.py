#!/usr/bin/python3
"""place reviews"""

from api.v1.views import app_views
import json
from models import storage
from flask import jsonify, make_response, request, abort
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def revs_all(place_id):
    """list all reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    listobj = []
    for obj in place.reviews:
        listobj.append(obj.to_dict())
    return jsonify(listobj)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def review_get(review_id):
    """review info"""
    elem = storage.get(Review, review_id)
    if not elem:
        abort(404)
    return jsonify(elem.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def review_del(review_id):
    """delete"""
    elem = storage.get(Review, review_id)
    if not elem:
        abort(404)
    storage.delete(elem)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_rev(place_id):
    """post"""
    req = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not req:
        abort(400, description="Not a JSON")
    if 'user_id' not in req:
        abort(400, description="Missing user_id")
    if not storage.get(User, req['user_id']):
        abort(404)
    if 'text' not in req:
        abort(400, description="Missing text")
    req["place_id"] = place_id
    info = Review(**req)
    info.save()
    return make_response(jsonify(info.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_rev(review_id):
    """put"""
    req = request.json
    if not req:
        abort(400, description="Not a JSON")
    if not storage.get(Review, review_id):
        abort(404)
    badkeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req.items():
        if key not in badkeys:
            elem = storage.get(Review, review_id)
            setattr(elem, key, value)
    storage.save()
    return make_response(jsonify(elem.to_dict()), 200)