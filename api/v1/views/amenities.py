#!/usr/bin/python3
"""RESTful API endpoints for Amenity resource management.

This module provides HTTP endpoints for handling CRUD operations on Amenity objects.
It includes routes for retrieving all amenities, fetching individual amenities,
creating new amenities, updating existing amenities, and deleting amenities from
the storage system.

The module integrates with Flask for routing and request handling, and uses a
persistent storage backend for data persistence.
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def list_all_amenities():
    """Retrieve all Amenity objects from storage.

    Fetches all Amenity instances currently stored in the database and returns
    them as a JSON array of amenity dictionaries.

    Returns:
        flask.Response: JSON response containing a list of all amenity objects,
            where each amenity is represented as a dictionary.
    """
    all_amenity_dict = storage.all(Amenity)
    all_data_amenity_list = [all_amenity_dict[x].to_dict() for x in all_amenity_dict]
    return jsonify(all_data_amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_a_amenity(amenity_id):
    """Retrieve a specific Amenity object by its unique identifier.

    Fetches a single Amenity instance from storage using the provided amenity ID.
    If the amenity exists, it is returned as a JSON object. If not found, a 404
    error is returned.

    Args:
        amenity_id (str): The unique identifier of the amenity to retrieve.

    Returns:
        flask.Response: JSON response containing the requested amenity object
            as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the amenity with the specified ID
            does not exist in storage (HTTP 404).
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_amenity(amenity_id):
    """Delete a specific Amenity object from storage.

    Removes the Amenity instance with the given ID from the storage system and
    persists the changes. If the amenity does not exist, a 404 error is returned.

    Args:
        amenity_id (str): The unique identifier of the amenity to delete.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            deletion.

    Raises:
        werkzeug.exceptions.NotFound: If the amenity with the specified ID
            does not exist in storage (HTTP 404).
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a new Amenity object and store it in the database.

    Accepts a JSON payload containing amenity attributes and creates a new Amenity
    instance. Validates that the request contains valid JSON and includes the
    required "name" field. The newly created amenity is persisted to storage.

    Returns:
        tuple: A tuple containing:
            - flask.Response: JSON response with the created amenity object and
              HTTP 201 status on success.
            - int: HTTP status code (201 for success).

    Raises:
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
            - The "name" field is missing from the request payload
              ("Missing name" error).
    """
    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    if not data_dict.get("name", None):
        return (jsonify({"error": "Missing name"}), 400)

    new_amenity = Amenity(**data_dict)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """Update a specific Amenity object with new attribute values.

    Modifies an existing Amenity instance by applying attributes from a JSON
    payload. Certain attributes (id, created_at, updated_at, __class__) are
    protected and cannot be modified. If the amenity does not exist, a 404 error
    is returned.

    Args:
        amenity_id (str): The unique identifier of the amenity to update.

    Returns:
        flask.Response: JSON response containing the updated amenity object
            as a dictionary with HTTP 200 status.

    Raises:
        werkzeug.exceptions.NotFound: If the amenity with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "created_at", "updated_at", "__class__"]

    for key, value in data_dict.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict())
