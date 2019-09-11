#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API
"""
from flask import Flask, json, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states
    """
    tmp_list = []
    for key, value in storage.all("State").items():
        tmp_list.append(value.to_dict())
    return json.dumps(tmp_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    """get state by id
    """
    for key, value in storage.all("State").items():
        if state_id == value.id:
            return value.to_dict()
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete state by id
    """
    for key, values in storage.all("State").items():
        if state_id in key:
            storage.delete(values)
            storage.save()
            return ({}, 200)
    abort(404)


@app_views.route('/states',  methods=['POST'], strict_slashes=False)
def post_state():
    """ ††† method HTTP POST json
    """
    try:
        new_dict = request.get_json()
    except:
        abort(description="Not a JSON", status=400)
    if type(new_dict) != dict:
        abort(description="Not a JSON", status=400)
    if "name" in new_dict.keys():
        new_state = State()
        new_state.name = new_dict["name"]
        storage.new(new_state)
        storage.save()
        return (new_state.to_dict(), 201)
    abort(400, description="Missing name")


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ ††† method HTTP PUT to update the state with id †††
    """

    try:
        new_dict = request.get_json()
    except:
        abort(description="Not a JSON", status=400)
    if type(new_dict) != dict:
        abort(description="Not a JSON", status=400)
    for key in ['id', 'created_at', 'updated_at']:
        if key in new_dict:
            del new_dict[key]
    for key, value in storage.all("State").items():
        if state_id == value.id:
            value.__dict__.update(new_dict)
            storage.save()
            return (value.to_dict(), 200)
    abort(404)