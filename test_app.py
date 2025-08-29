import unittest
import json
import os
import tempfile
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Use a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        
        # Replace the progress manager with one using temp file
        from app import progress_manager
        progress_manager.data_file = self.temp_file.name
        progress_manager._ensure_data_file_exists()

    def tearDown(self):
        # Clean up temp file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)

    def test_get_progress_api(self):
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('completed_sessions', data)
        self.assertIn('total_focus_time', data)
        self.assertIn('today', data)

    def test_complete_session_api(self):
        # First, complete a session
        response = self.app.post('/api/complete', 
                                json={'focus_time_minutes': 25},
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['completed_sessions'], 1)
        self.assertEqual(data['total_focus_time'], 25)

    def test_update_progress_api(self):
        # Update progress data
        update_data = {'completed_sessions': 3, 'total_focus_time': 75}
        response = self.app.post('/api/progress',
                                json=update_data,
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['completed_sessions'], 3)
        self.assertEqual(data['total_focus_time'], 75)

    def test_update_progress_api_no_data(self):
        # Test error handling for no data
        response = self.app.post('/api/progress',
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
