#!/usr/bin/python3
"""RESTful API endpoints for Review resource management.

This module provides HTTP endpoints for handling CRUD operations on Review objects.
It includes routes for retrieving reviews for a specific place, fetching individual
reviews, creating new reviews, updating existing reviews, and deleting reviews from
the storage system. Each review is associated with a parent Place and an author User.

The module integrates with Flask for routing and request handling, and uses a
persistent storage backend for data persistence.
"""

from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def list_reviews_of_place(place_id):
    """Retrieve all Review objects associated with a specific Place.

    Fetches all Review instances that belong to the given place. The place must
    exist in storage; otherwise, a 404 error is returned. The reviews are
    returned as a JSON array of review dictionaries.

    Args:
        place_id (str): The unique identifier of the parent place whose reviews
            will be retrieved.

    Returns:
        flask.Response: JSON response containing a list of all reviews belonging
            to the specified place, where each review is represented as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the place with the specified ID
            does not exist in storage (HTTP 404).
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    all_reviews_of_place_list = [x.to_dict() for x in place.reviews]
    return jsonify(all_reviews_of_place_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_a_review(review_id):
    """Retrieve a specific Review object by its unique identifier.

    Fetches a single Review instance from storage using the provided review ID.
    If the review exists, it is returned as a JSON object. If not found, a 404
    error is returned.

    Args:
        review_id (str): The unique identifier of the review to retrieve.

    Returns:
        flask.Response: JSON response containing the requested review object
            as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the review with the specified ID
            does not exist in storage (HTTP 404).
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_review(review_id):
    """Delete a specific Review object from storage.

    Removes the Review instance with the given ID from the storage system and
    persists the changes. If the review does not exist, a 404 error is returned.

    Args:
        review_id (str): The unique identifier of the review to delete.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            deletion.

    Raises:
        werkzeug.exceptions.NotFound: If the review with the specified ID
            does not exist in storage (HTTP 404).
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({})
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Create a new Review object and associate it with a specific Place.

    Accepts a JSON payload containing review attributes and creates a new Review
    instance linked to the specified parent place. Validates that the place exists,
    the request contains valid JSON, the required "user_id" field references a
    valid User, and the required "text" field is present. The place_id is
    automatically assigned to the new review. The newly created review is persisted
    to storage.

    Args:
        place_id (str): The unique identifier of the parent place to which
            the new review will be associated.

    Returns:
        tuple: A tuple containing:
            - flask.Response: JSON response with the created review object and
              HTTP 201 status on success.
            - int: HTTP status code (201 for success).

    Raises:
        werkzeug.exceptions.NotFound: If:
            - The place with the specified ID does not exist in storage (HTTP 404).
            - The user_id from the request payload does not reference a valid
              user in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
            - The "user_id" field is missing from the request payload
              ("Missing user_id" error).
            - The "text" field is missing from the request payload
              ("Missing text" error).
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    if not data_dict.get("user_id", None):
        return (jsonify({"error": "Missing user_id"}), 400)

    user = storage.get(User, data_dict["user_id"])
    if not user:
        abort(404)

    if not data_dict.get("text", None):
        return (jsonify({"error": "Missing text"}), 400)

    data_dict["place_id"] = place_id
    new_review = Review(**data_dict)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Update a specific Review object with new attribute values.

    Modifies an existing Review instance by applying attributes from a JSON
    payload. Certain attributes (id, created_at, updated_at, __class__, place_id,
    user_id) are protected and cannot be modified. The parent place and author user
    associations are immutable. If the review does not exist, a 404 error is returned.

    Args:
        review_id (str): The unique identifier of the review to update.

    Returns:
        flask.Response: JSON response containing the updated review object
            as a dictionary with HTTP 200 status.

    Raises:
        werkzeug.exceptions.NotFound: If the review with the specified ID
            does not exist in storage (HTTP 404).
        werkzeug.exceptions.BadRequest: Returns HTTP 400 with error message if:
            - The request body is not valid JSON ("Not a JSON" error).
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    data_dict = request.get_json(silent=True)
    if not data_dict:
        return (jsonify({"error": "Not a JSON"}), 400)

    ignored_keys = ["id", "created_at", "updated_at", "__class__", "place_id", "user_id"]

    for key, value in data_dict.items():
        if key not in ignored_keys:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict())
