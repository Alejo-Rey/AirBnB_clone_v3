#!/usr/bin/python3
"""Create a new view for State objects that handles all default RestFul API
"""
from flask import Flask, json, jsonify, abort
from api.v1.views import app_views
from models import storage


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
