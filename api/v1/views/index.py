#!/usr/bin/python3
"""
This module defines API endpoints for retrieving status and statistics.

The module includes two endpoints:
- `/status`: Returns a JSON response indicating the API is running.
- `/stats`: Returns a JSON response with the count of various object types.

These endpoints are part of the AirBnB clone project and are used to
monitor the health and basic statistics of the application.
"""

from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', strict_slashes=False)
def status():
    """
    Endpoint to check the API status.

    This route is used to verify if the API service is up and running.
    It returns a simple JSON object with a key-value pair indicating status.

    Returns:
        Response: A Flask JSON response with status information.
        Example response: {"status": "OK"}
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def count():
    """
    Endpoint to retrieve counts of different object types.

    This route provides a count of each type of object stored in the database.
    It returns a JSON object with the counts of amenities, cities, places, reviews, states, and users.

    Returns:
        Response: A Flask JSON response with counts of various objects.
        Example response: {
            "amenities": 10,
            "cities": 5,
            "places": 15,
            "reviews": 50,
            "states": 3,
            "users": 100
        }
    """
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
