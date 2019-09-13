#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_place(city_id):
    """get all places of a id city
    """
    new_list = []
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for key, values in storage.all("Place").items():
        if city_id == values.city_id:
            new_list.append(values.to_dict())

    return jsonify(new_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places_id(place_id):
    """get place by id
    """
    for key, values in storage.all("Place").items():
        if place_id == values.id:
            return jsonify(values.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_places(place_id):
    """delete place by id
    """
    for key, values in storage.all("Place").items():
        if place_id in key:
            storage.delete(values)
            storage.save()
            storage.close()
            return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_places(city_id):
    """ ††† method HTTP POST json
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400

    if "user_id" not in new_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if "name" not in new_dict:
        return jsonify({"error": "Missing name"}), 400
    user = storage.get("User", new_dict["user_id"])
    if user is None:
        abort(404)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    new_place = Place()
    for k, v in new_dict.items():
        setattr(new_place, k, v)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_places(city_id):
    """ ††† method HTTP PUT to update the City with id †††
    """
    if request.is_json:
        new_dict = request.get_json()
    else:
        return jsonify({"error": "Not a JSON"}), 400
    for key in ['id', 'created_at', 'updated_at', 'state_id']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("City").items():
        if city_id == value.id:
            for k, v in new_dict.items():
                setattr(value, k, v)
            storage.save()
            return jsonify(value.to_dict()), 200
    abort(404)
