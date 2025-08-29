"""
Basic test for app functionality - moved to tests/test_api.py for more comprehensive testing
"""
import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)
        self.assertIn('ポモドーロタイマー'.encode('utf-8'), response.data)

    def test_timer_js_included(self):
        """Test that timer.js is included in the HTML"""
        response = self.app.get('/')
        self.assertIn(b'timer.js', response.data)

if __name__ == '__main__':
    unittest.main()
