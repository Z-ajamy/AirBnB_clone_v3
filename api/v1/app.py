#!/usr/bin/python3
"""
Main Flask Application for AirBnB Clone v3 API
"""
from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/*" : {"origins" : "0.0.0.0"}})
app.register_blueprint(app_views)

@app.teardown_appcontext
def tear_down(error):
    """
    Closes the storage session after each request
    """
    storage.close()


@app.errorhandler(404)
def err404(error):
    """
    handler for 404 errors that returns a JSON-formatted 404 status code
    response.
    """
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')

    app.run(host=host, port=int(port), threaded=True, debug=True)

