#!/usr/bin/python3
"""RESTful API endpoints for City resource management.

This module provides HTTP endpoints for handling CRUD operations on City objects.
It includes routes for retrieving cities within a specific state, fetching individual
cities, creating new cities, updating existing cities, and deleting cities from the
storage system. Each city is associated with a parent State.

The module integrates with Flask for routing and request handling, and uses a
persistent storage backend for data persistence.
"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def list_cities_of_state(state_id):
    """Retrieve all City objects associated with a specific State.

    Fetches all City instances that belong to the given state. The state must
    exist in storage; otherwise, a 404 error is returned. The cities are
    returned as a JSON array of city dictionaries.

    Args:
        state_id (str): The unique identifier of the parent state whose cities
            will be retrieved.

    Returns:
        flask.Response: JSON response containing a list of all cities belonging
            to the specified state, where each city is represented as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the state with the specified ID
            does not exist in storage (HTTP 404).
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    all_cities_of_state_list = [x.to_dict() for x in state.cities]
    return jsonify(all_cities_of_state_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_a_city(city_id):
    """Retrieve a specific City object by its unique identifier.

    Fetches a single City instance from storage using the provided city ID.
    If the city exists, it is returned as a JSON object. If not found, a 404
    error is returned.

    Args:
        city_id (str): The unique identifier of the city to retrieve.

    Returns:
        flask.Response: JSON response containing the requested city object
            as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the city with the specified ID
            does not exist in storage (HTTP 404).
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_city(city_id):
    """Delete a specific City object from storage.

    Removes the City instance with the given ID from the storage system and
    persists the changes. If the city does not exist, a 404 error is returned.

    Args:
        city_id (str): The unique identifier of the city to delete.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            deletion.

    Raises:
        werkzeug.exceptions.NotFound: If the city with the specified ID
            does not exist in storage (HTTP 404).
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """Create a new City object and associate it with a specific State.

    Accepts a JSON payload containing city attributes and creates a new City
    instance linked to the specified parent state. Validates that the state
    exists, the request contains valid JSON, and includes the required "name"
    field. The state_id is automatically assigned to the new city. The newly
    created city is persisted to storage.

    Args:
        state_id (str): The unique identifier of the parent state to which
            the new city will be associated.

    Returns:
        tuple: A tuple containing:
            - flask.Response: JSON response with the created city object and
              HTTP 201 status on success.
            - int: HTTP status code (201 for success).

    Raises:
        werkzeug.exceptions.NotFound: If the state with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
            - The "name" field is missing from the request payload
              ("Missing name" error).
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    if not data_dict.get("name", None):
        return (jsonify({"error": "Missing name"}), 400)

    data_dict["state_id"] = state_id
    new_city = City(**data_dict)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """Update a specific City object with new attribute values.

    Modifies an existing City instance by applying attributes from a JSON
    payload. Certain attributes (id, created_at, updated_at, __class__,
    state_id) are protected and cannot be modified. The parent state association
    is immutable. If the city does not exist, a 404 error is returned.

    Args:
        city_id (str): The unique identifier of the city to update.

    Returns:
        flask.Response: JSON response containing the updated city object
            as a dictionary with HTTP 200 status.

    Raises:
        werkzeug.exceptions.NotFound: If the city with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "created_at", "updated_at", "__class__", "state_id"]

    for key, value in data_dict.items():
        if key not in ignored_keys:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_dict())
