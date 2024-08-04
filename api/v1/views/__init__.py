#!/usr/bin/python3
"""
Initialize the blueprint for the API views
"""
from api.v1.views import index  # Import routes from index.py
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
