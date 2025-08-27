import unittest
import json
import os
import tempfile
from app import app
from services.progress_manager import ProgressManager

class ProgressAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, "test_progress.json")
        
        # Use a test-specific progress manager
        app.config['TESTING'] = True
        self.test_progress_manager = ProgressManager(self.test_data_file)
        
        # Replace the app's progress manager with test one
        import app as app_module
        app_module.progress_manager = self.test_progress_manager

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        os.rmdir(self.temp_dir)

    def test_get_progress_initial(self):
        """Test getting initial progress data"""
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('completed_sessions', data)
        self.assertIn('total_focus_time', data)
        self.assertIn('last_updated', data)
        self.assertEqual(data['completed_sessions'], 0)
        self.assertEqual(data['total_focus_time'], 0)

    def test_update_progress_with_data(self):
        """Test updating progress with specific data"""
        update_data = {
            'completed_sessions': 5,
            'total_focus_time': 125
        }
        
        response = self.app.post('/api/progress', 
                               data=json.dumps(update_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['completed_sessions'], 5)
        self.assertEqual(data['total_focus_time'], 125)

    def test_add_session(self):
        """Test adding a completed session"""
        update_data = {
            'action': 'add_session',
            'session_duration': 25
        }
        
        response = self.app.post('/api/progress', 
                               data=json.dumps(update_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['completed_sessions'], 1)
        self.assertEqual(data['total_focus_time'], 25)

    def test_reset_progress(self):
        """Test resetting progress"""
        # First add some data
        update_data = {'completed_sessions': 5, 'total_focus_time': 125}
        self.app.post('/api/progress', 
                     data=json.dumps(update_data),
                     content_type='application/json')
        
        # Then reset
        reset_data = {'action': 'reset'}
        response = self.app.post('/api/progress', 
                               data=json.dumps(reset_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['completed_sessions'], 0)
        self.assertEqual(data['total_focus_time'], 0)

    def test_post_without_data(self):
        """Test POST request without data"""
        response = self.app.post('/api/progress')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_progress_persistence(self):
        """Test that progress data persists between requests"""
        # Add a session
        update_data = {
            'action': 'add_session',
            'session_duration': 30
        }
        self.app.post('/api/progress', 
                     data=json.dumps(update_data),
                     content_type='application/json')
        
        # Check that it persists
        response = self.app.get('/api/progress')
        data = json.loads(response.data)
        self.assertEqual(data['completed_sessions'], 1)
        self.assertEqual(data['total_focus_time'], 30)

if __name__ == '__main__':
    unittest.main()