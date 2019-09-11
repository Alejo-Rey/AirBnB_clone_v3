#!/usr/bin/python3
''' funtion using flask '''
from flask import Flask
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

if __name__ == '__main__':
    app.run(host=os.environ['HBNB_API_HOST'],
            port=os.environ['HBNB_API_PORT'], threaded=True)
