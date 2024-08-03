#!/usr/bin/python3
"""
Create a Flask app for the API
"""

from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    from os import getenv

    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', 5000)
    app.run(host=HBNB_API_HOST, port=int(HBNB_API_PORT), threaded=True)
