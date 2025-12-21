#!/usr/bin/python3
"""
Index view for the API
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route("/status")
def statusok():
    return jsonify({"status": "OK"})
