import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        # Test for Japanese text in the response
        response_text = response.data.decode('utf-8')
        self.assertIn('ポモドーロタイマー', response_text)
    
    def test_progress_api_get(self):
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('completed_sessions', data)
        self.assertIn('focus_time', data)
        self.assertIn('date', data)
    
    def test_progress_api_post(self):
        response = self.app.post('/api/progress', 
                                json={'session_duration': 25})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('completed_sessions', data)
        self.assertIn('focus_time', data)

if __name__ == '__main__':
    unittest.main()
