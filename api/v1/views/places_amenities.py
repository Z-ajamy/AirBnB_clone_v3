#!/usr/bin/python3
"""RESTful API endpoints for Place-Amenity relationship management.

This module provides HTTP endpoints for managing the many-to-many relationship
between Place and Amenity objects. It includes routes for retrieving amenities
associated with a place, linking new amenities to a place, and unlinking amenities
from a place.

The module supports both database storage (via SQLAlchemy relationships) and
file-based storage (via list attributes) through environment-based configuration.
It integrates with Flask for routing and request handling, and uses a persistent
storage backend for data persistence.
"""

from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from os import environ


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieve all Amenity objects associated with a specific Place.

    Fetches all Amenity instances linked to the given place. The place must
    exist in storage; otherwise, a 404 error is returned. The function adapts
    its behavior based on the storage type: database storage uses relationship
    navigation, while file-based storage uses amenity ID lists.

    Args:
        place_id (str): The unique identifier of the place whose amenities
            will be retrieved.

    Returns:
        flask.Response: JSON response containing a list of all amenities
            associated with the specified place, where each amenity is
            represented as a dictionary.

    Raises:
        werkzeug.exceptions.NotFound: If the place with the specified ID
            does not exist in storage (HTTP 404).
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, a_id).to_dict()
                     for a_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Unlink a specific Amenity from a Place.

    Removes the association between an amenity and a place. Both the place and
    amenity must exist in storage; otherwise, a 404 error is returned. If the
    amenity is not currently linked to the place, a 404 error is also returned.
    The function adapts its behavior based on the storage type: database storage
    removes the object from the relationship collection, while file-based storage
    removes the amenity ID from the list.

    Args:
        place_id (str): The unique identifier of the place from which the
            amenity will be unlinked.
        amenity_id (str): The unique identifier of the amenity to unlink from
            the place.

    Returns:
        flask.Response: Empty JSON object with HTTP 200 status on successful
            unlinking.

    Raises:
        werkzeug.exceptions.NotFound: If:
            - The place with the specified ID does not exist in storage (HTTP 404).
            - The amenity with the specified ID does not exist in storage (HTTP 404).
            - The amenity is not currently linked to the place (HTTP 404).
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Link a specific Amenity to a Place.

    Creates an association between an amenity and a place. Both the place and
    amenity must exist in storage; otherwise, a 404 error is returned. If the
    amenity is already linked to the place, the existing link is returned with
    HTTP 200 status. Otherwise, the new link is created and returned with HTTP
    201 status. The function adapts its behavior based on the storage type:
    database storage appends to the relationship collection, while file-based
    storage appends the amenity ID to the list.

    Args:
        place_id (str): The unique identifier of the place to which the
            amenity will be linked.
        amenity_id (str): The unique identifier of the amenity to link to
            the place.

    Returns:
        flask.Response: JSON response containing the amenity object and either:
            - HTTP 200 status if the amenity was already linked to the place.
            - HTTP 201 status if the amenity was newly linked to the place.

    Raises:
        werkzeug.exceptions.NotFound: If:
            - The place with the specified ID does not exist in storage (HTTP 404).
            - The amenity with the specified ID does not exist in storage (HTTP 404).
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if not place or not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
