#!/usr/bin/python3
"""RESTful API endpoints for State resource management.

This module provides HTTP endpoints for handling CRUD operations on State objects.
It includes routes for retrieving all states, fetching individual states, creating
new states, updating existing states, and deleting states from the storage system.

The module integrates with Flask for routing and request handling, and uses a
persistent storage backend for data persistence.
"""


from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def list_all_states():
    """Retrieve all State objects from storage.

    Fetches all State instances currently stored in the database and returns
    them as a JSON array of state dictionaries.

    Returns:
        flask.Response: JSON response containing a list of all state objects,
            where each state is represented as a dictionary.
    """
    all_state_dict = storage.all(State)
    all_data_state_list = [all_state_dict[x].to_dict() for x in all_state_dict]
    return jsonify(all_data_state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_a_state(state_id):
    """Retrieve a specific State object by its unique identifier.

    Fetches a single State instance from storage using the provided state ID.
    If the state exists, it is returned as a JSON object. If not found, a 404
    error is returned.

    Args:
        state_id (str): The unique identifier of the state to retrieve.

    Returns:
        flask.Response: JSON response containing the requested state object
            as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the state with the specified ID
            does not exist in storage (HTTP 404).
    """
    state = storage.get(State, str(state_id))
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_state(state_id):
    """Delete a specific State object from storage.

    Removes the State instance with the given ID from the storage system and
    persists the changes. If the state does not exist, a 404 error is returned.

    Args:
        state_id (str): The unique identifier of the state to delete.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            deletion.

    Raises:
        werkzeug.exceptions.NotFound: If the state with the specified ID
            does not exist in storage (HTTP 404).
    """
    state = storage.get(State, str(state_id))
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new State object and store it in the database.

    Accepts a JSON payload containing state attributes and creates a new State
    instance. Validates that the request contains valid JSON and includes the
    required "name" field. The newly created state is persisted to storage.

    Returns:
        tuple: A tuple containing:
            - flask.Response: JSON response with the created state object and
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

    new_state = State(**data_dict)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update a specific State object with new attribute values.

    Modifies an existing State instance by applying attributes from a JSON
    payload. Certain attributes (id, created_at, updated_at, __class__) are
    protected and cannot be modified. If the state does not exist, a 404 error
    is returned.

    Args:
        state_id (str): The unique identifier of the state to update.

    Returns:
        flask.Response: JSON response containing the updated state object
            as a dictionary with HTTP 200 status.

    Raises:
        werkzeug.exceptions.NotFound: If the state with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "created_at", "updated_at", "__class__"]

    for key, value in data_dict.items():
        if key not in ignored_keys:
            setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict())
