#!/usr/bin/python3
"""
Unittest for API app.py
"""

import unittest
from api.v1.app import app


class TestApp(unittest.TestCase):
    """Test the app configurations and routes"""

    def setUp(self):
        """Set up the test client"""
        self.client = app.test_client()
        self.client.testing = True

    def test_app_configuration(self):
        """Test the app configuration"""
        self.assertEqual(app.config['JSONIFY_PRETTYPRINT_REGULAR'], False)
        self.assertEqual(app.url_map.default_subdomain, '')

    def test_404_error(self):
        """Test the 404 error handler"""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")


if __name__ == '__main__':
    unittest.main()
