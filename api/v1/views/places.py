#!/usr/bin/python3
"""RESTful API endpoints for Place resource management.

This module provides HTTP endpoints for handling CRUD operations on Place objects.
It includes routes for retrieving places within a specific city, fetching individual
places, creating new places, updating existing places, and deleting places from the
storage system. Each place is associated with a parent City and an owner User.

The module integrates with Flask for routing and request handling, and uses a
persistent storage backend for data persistence.
"""

from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def list_places_of_city(city_id):
    """Retrieve all Place objects associated with a specific City.

    Fetches all Place instances that belong to the given city. The city must
    exist in storage; otherwise, a 404 error is returned. The places are
    returned as a JSON array of place dictionaries.

    Args:
        city_id (str): The unique identifier of the parent city whose places
            will be retrieved.

    Returns:
        flask.Response: JSON response containing a list of all places belonging
            to the specified city, where each place is represented as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the city with the specified ID
            does not exist in storage (HTTP 404).
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    all_places_of_city_list = [x.to_dict() for x in city.places]
    return jsonify(all_places_of_city_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_a_place(place_id):
    """Retrieve a specific Place object by its unique identifier.

    Fetches a single Place instance from storage using the provided place ID.
    If the place exists, it is returned as a JSON object. If not found, a 404
    error is returned.

    Args:
        place_id (str): The unique identifier of the place to retrieve.

    Returns:
        flask.Response: JSON response containing the requested place object
            as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the place with the specified ID
            does not exist in storage (HTTP 404).
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_place(place_id):
    """Delete a specific Place object from storage.

    Removes the Place instance with the given ID from the storage system and
    persists the changes. If the place does not exist, a 404 error is returned.

    Args:
        place_id (str): The unique identifier of the place to delete.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            deletion.

    Raises:
        werkzeug.exceptions.NotFound: If the place with the specified ID
            does not exist in storage (HTTP 404).
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Create a new Place object and associate it with a specific City.

    Accepts a JSON payload containing place attributes and creates a new Place
    instance linked to the specified parent city. Validates that the city exists,
    the request contains valid JSON, the required "user_id" field references a
    valid User, and the required "name" field is present. The city_id is
    automatically assigned to the new place. The newly created place is persisted
    to storage.

    Args:
        city_id (str): The unique identifier of the parent city to which
            the new place will be associated.

    Returns:
        tuple: A tuple containing:
            - flask.Response: JSON response with the created place object and
              HTTP 201 status on success.
            - int: HTTP status code (201 for success).

    Raises:
        werkzeug.exceptions.NotFound: If:
            - The city with the specified ID does not exist in storage (HTTP 404).
            - The user_id from the request payload does not reference a valid
              user in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
            - The "user_id" field is missing from the request payload
              ("Missing user_id" error).
            - The "name" field is missing from the request payload
              ("Missing name" error).
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    if not data_dict.get("user_id", None):
        return (jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, data_dict["user_id"])
    if not user:
        abort(404)

    if not data_dict.get("name", None):
        return (jsonify({"error": "Missing name"}), 400)

    data_dict["city_id"] = city_id
    new_place = Place(**data_dict)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update a specific Place object with new attribute values.

    Modifies an existing Place instance by applying attributes from a JSON
    payload. Certain attributes (id, created_at, updated_at, __class__, user_id,
    city_id) are protected and cannot be modified. The owner user and parent
    city associations are immutable. If the place does not exist, a 404 error
    is returned.

    Args:
        place_id (str): The unique identifier of the place to update.

    Returns:
        flask.Response: JSON response containing the updated place object
            as a dictionary with HTTP 200 status.

    Raises:
        werkzeug.exceptions.NotFound: If the place with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "created_at", "updated_at", "__class__", "user_id", "city_id"]

    for key, value in data_dict.items():
        if key not in ignored_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict())
