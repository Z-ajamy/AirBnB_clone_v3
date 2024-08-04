#!/usr/bin/python3
"""
Index route for the API
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/status', methods=['GET'])
def status():
    """Return the status of the API"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the number of each object type"""
    object_counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(object_counts)
