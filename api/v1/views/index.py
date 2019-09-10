#!/usr/bin/python3
""" create a route /status on the object app_views that returns a JSON
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def json_return():
    return jsonify({
                    "status": "OK"
                    })
