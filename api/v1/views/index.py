#!/usr/bin/python3
"""
Index view for the API
"""

from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from api.v1.views import app_views
from flask import jsonify



classes = {"amenity": Amenity, "city": City,
           "place": Place, "review": Review, "state": State, "user": User}


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def count():
    """
    Retrieves the number of each objects by type
    """
    stats = {}
    for key in classes:
        stats[key] = storage.count(classes[key])
    return jsonify(stats)
