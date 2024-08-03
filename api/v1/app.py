#!/usr/bin/python3
"""
This module contains the principal application
"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': 'This is the API created for the hbnb restful API project.\
    All the documentation will be shown below.',
    'uiversion': 3
}
swagger = Swagger(app)


@app.teardown_appcontext
def close_db(exception):
    """Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handles 404 errors with a custom message"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=int(port), threaded=True)
