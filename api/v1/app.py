#!/usr/bin/python3
"""
This module contains the principal application for the AirBnB clone - RESTful API.

The application uses Flask to create a web server with several endpoints and includes:
- Integration with models to handle database interactions.
- Blueprint registration for organizing routes.
- Cross-Origin Resource Sharing (CORS) setup.
- Swagger for API documentation.

Environment variables used:
- HBNB_API_HOST: Defines the host address for the API server. Defaults to '0.0.0.0'.
- HBNB_API_PORT: Defines the port number for the API server. Defaults to 5000.
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_db(obj):
    """ 
    Closes the storage engine after each request.
    
    This function is called automatically at the end of each request's context
    to ensure that any open database connections are properly closed.
    """
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """ 
    Handles 404 errors by returning a JSON response.
    
    This function provides a custom JSON response when a requested resource is not found.
    
    Args:
        error (Exception): The error that triggered this handler.
    
    Returns:
        Response: A Flask response object with a 404 status code and JSON payload.
    """
    return make_response(jsonify({"error": "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone - RESTful API',
    'description': ('This is the API that was created for the hbnb restful API project, '
                    'all the documentation will be shown below.'),
    'uiversion': 3
}

Swagger(app)

if __name__ == "__main__":
    # Set up the host and port from environment variables or use defaults
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    # Run the Flask application
    app.run(host, int(port), threaded=True)
