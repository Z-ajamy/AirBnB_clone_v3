#!/usr/bin/python3
"""RESTful API endpoints for User resource management.

This module provides HTTP endpoints for handling CRUD operations on User objects.
It includes routes for retrieving all users, fetching individual users, creating
new users, updating existing users, and deleting users from the storage system.

The module integrates with Flask for routing and request handling, and uses a
persistent storage backend for data persistence.
"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def list_all_users():
    """Retrieve all User objects from storage.

    Fetches all User instances currently stored in the database and returns
    them as a JSON array of user dictionaries.

    Returns:
        flask.Response: JSON response containing a list of all user objects,
            where each user is represented as a dictionary.
    """
    all_user_dict = storage.all(User)
    all_data_user_list = [user.to_dict() for user in all_user_dict.values()]
    return jsonify(all_data_user_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_a_user(user_id):
    """Retrieve a specific User object by its unique identifier.

    Fetches a single User instance from storage using the provided user ID.
    If the user exists, it is returned as a JSON object. If not found, a 404
    error is returned.

    Args:
        user_id (str): The unique identifier of the user to retrieve.

    Returns:
        flask.Response: JSON response containing the requested user object
            as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the user with the specified ID
            does not exist in storage (HTTP 404).
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_user(user_id):
    """Delete a specific User object from storage.

    Removes the User instance with the given ID from the storage system and
    persists the changes. If the user does not exist, a 404 error is returned.

    Args:
        user_id (str): The unique identifier of the user to delete.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            deletion.

    Raises:
        werkzeug.exceptions.NotFound: If the user with the specified ID
            does not exist in storage (HTTP 404).
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new User object and store it in the database.

    Accepts a JSON payload containing user attributes and creates a new User
    instance. Validates that the request contains valid JSON and includes the
    required "email" and "password" fields. The newly created user is persisted
    to storage.

    Returns:
        tuple: A tuple containing:
            - flask.Response: JSON response with the created user object and
              HTTP 201 status on success.
            - int: HTTP status code (201 for success).

    Raises:
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
            - The "email" field is missing from the request payload
              ("Missing email" error).
            - The "password" field is missing from the request payload
              ("Missing password" error).
    """
    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    if not data_dict.get("email", None):
        return (jsonify({"error": "Missing email"}), 400)

    if not data_dict.get("password", None):
        return (jsonify({"error": "Missing password"}), 400)

    new_user = User(**data_dict)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update a specific User object with new attribute values.

    Modifies an existing User instance by applying attributes from a JSON
    payload. Certain attributes (id, created_at, updated_at, __class__, email)
    are protected and cannot be modified. The user's email address is immutable
    for security purposes. If the user does not exist, a 404 error is returned.

    Args:
        user_id (str): The unique identifier of the user to update.

    Returns:
        flask.Response: JSON response containing the updated user object
            as a dictionary with HTTP 200 status.

    Raises:
        werkzeug.exceptions.NotFound: If the user with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "created_at", "updated_at", "__class__", "email"]

    for key, value in data_dict.items():
        if key not in ignored_keys:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_dict())
