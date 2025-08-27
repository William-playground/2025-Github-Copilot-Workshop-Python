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
    
    def test_timer_javascript_included(self):
        """Test that the timer JavaScript file is included in the HTML"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/static/js/timer.js', response.data)
    
    def test_circular_progress_elements(self):
        """Test that the HTML contains elements needed for circular progress"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for timer elements with IDs
        self.assertIn(b'id="time"', response.data)
        self.assertIn(b'id="start"', response.data)
        self.assertIn(b'id="reset"', response.data)
        # Check for progress container
        self.assertIn(b'class="progress"', response.data)
    
    def test_css_file_included(self):
        """Test that the CSS file is included in the HTML"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/static/css/style.css', response.data)

if __name__ == '__main__':
    unittest.main()
