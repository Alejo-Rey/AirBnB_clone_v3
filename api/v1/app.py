#!/usr/bin/python3
''' funtion using flask '''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

app.strict_slashes = False


@app.teardown_appcontext
def close_method(exception=None):
    ''' close ssesions '''
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    """††† return 404 not found †††
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    app.run(host=os.environ['HBNB_API_HOST'],
            port=os.environ['HBNB_API_PORT'], threaded=True)
