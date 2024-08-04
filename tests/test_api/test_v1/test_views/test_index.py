#!/usr/bin/python3
"""
Unittest for API index routes
"""

import unittest
from api.v1.app import app
from flask import json


class TestIndex(unittest.TestCase):
    """Test the /status and /stats endpoints"""

    def setUp(self):
        """Set up the test client"""
        self.client = app.test_client()
        self.client.testing = True

    def test_status(self):
        """Test the /status route"""
        response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertEqual(json.loads(response.data), {"status": "OK"})

    def test_stats(self):
        """Test the /stats route"""
        response = self.client.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        # Add checks for expected keys and types
        data = json.loads(response.data)
        expected_keys = ["amenities", "cities", "places", "reviews", "states", "users"]
        for key in expected_keys:
            self.assertIn(key, data)
            self.assertIsInstance(data[key], int)


if __name__ == '__main__':
    unittest.main()
