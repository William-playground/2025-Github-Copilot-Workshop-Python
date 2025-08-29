"""
Unit tests for Flask API endpoints
"""
import unittest
import json
import tempfile
import os
from app import app
from services.progress_manager import ProgressManager


class TestFlaskAPI(unittest.TestCase):
    """Test cases for Flask API endpoints"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Use temporary file for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_progress.json")
        
        # Replace the progress manager with test instance
        app.config['TESTING'] = True
        
        # Import here to avoid circular import
        import app as app_module
        self.original_progress_manager = app_module.progress_manager
        app_module.progress_manager = ProgressManager(self.test_file)
    
    def tearDown(self):
        """Clean up test environment"""
        # Restore original progress manager
        import app as app_module
        app_module.progress_manager = self.original_progress_manager
        
        # Clean up test files
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.test_dir)
    
    def test_index_route(self):
        """Test the index route returns HTML"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)
        self.assertIn('ポモドーロタイマー'.encode('utf-8'), response.data)
    
    def test_get_progress_initial(self):
        """Test getting initial progress data"""
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)
        
        progress = data['data']
        self.assertEqual(progress['today_completed'], 0)
        self.assertEqual(progress['today_focus_time'], 0)
        self.assertEqual(progress['total_completed'], 0)
        self.assertEqual(progress['total_focus_time'], 0)
    
    def test_post_progress_complete_session(self):
        """Test completing a session via POST"""
        response = self.app.post('/api/progress',
                                data=json.dumps({
                                    'action': 'complete_session',
                                    'focus_time': 25
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        
        progress = data['data']
        self.assertEqual(progress['today_completed'], 1)
        self.assertEqual(progress['today_focus_time'], 25)
        self.assertEqual(progress['total_completed'], 1)
        self.assertEqual(progress['total_focus_time'], 25)
    
    def test_post_progress_complete_session_custom_time(self):
        """Test completing a session with custom focus time"""
        response = self.app.post('/api/progress',
                                data=json.dumps({
                                    'action': 'complete_session',
                                    'focus_time': 30
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        progress = data['data']
        self.assertEqual(progress['today_completed'], 1)
        self.assertEqual(progress['today_focus_time'], 30)
    
    def test_post_progress_reset_today(self):
        """Test resetting today's progress"""
        # First, add some progress
        self.app.post('/api/progress',
                     data=json.dumps({
                         'action': 'complete_session',
                         'focus_time': 25
                     }),
                     content_type='application/json')
        
        # Then reset
        response = self.app.post('/api/progress',
                                data=json.dumps({
                                    'action': 'reset_today'
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        progress = data['data']
        self.assertEqual(progress['today_completed'], 0)
        self.assertEqual(progress['today_focus_time'], 0)
        # Total should remain
        self.assertEqual(progress['total_completed'], 1)
        self.assertEqual(progress['total_focus_time'], 25)
    
    def test_post_progress_general_update(self):
        """Test general progress update"""
        response = self.app.post('/api/progress',
                                data=json.dumps({
                                    'today_completed': 3,
                                    'today_focus_time': 75,
                                    'custom_field': 'test'
                                }),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        progress = data['data']
        self.assertEqual(progress['today_completed'], 3)
        self.assertEqual(progress['today_focus_time'], 75)
        self.assertEqual(progress['custom_field'], 'test')
    
    def test_post_progress_no_data(self):
        """Test POST request with no data"""
        response = self.app.post('/api/progress',
                                content_type='application/json')
        
        # Should return an error (either 400 or 500 is acceptable for this test)
        self.assertGreaterEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)
    
    def test_post_progress_invalid_json(self):
        """Test POST request with invalid JSON"""
        response = self.app.post('/api/progress',
                                data='invalid json',
                                content_type='application/json')
        
        # Should return an error (either 400 or 500 is acceptable for this test)
        self.assertGreaterEqual(response.status_code, 400)
    
    def test_multiple_sessions(self):
        """Test multiple session completions"""
        # Complete first session
        response1 = self.app.post('/api/progress',
                                 data=json.dumps({
                                     'action': 'complete_session',
                                     'focus_time': 25
                                 }),
                                 content_type='application/json')
        
        # Complete second session
        response2 = self.app.post('/api/progress',
                                 data=json.dumps({
                                     'action': 'complete_session',
                                     'focus_time': 30
                                 }),
                                 content_type='application/json')
        
        # Check final state
        response3 = self.app.get('/api/progress')
        
        data = json.loads(response3.data)
        progress = data['data']
        self.assertEqual(progress['today_completed'], 2)
        self.assertEqual(progress['today_focus_time'], 55)
        self.assertEqual(progress['total_completed'], 2)
        self.assertEqual(progress['total_focus_time'], 55)
    
    def test_api_error_handling(self):
        """Test API error handling with invalid operations"""
        # Simulate error by using non-existent directory
        import app as app_module
        app_module.progress_manager.data_file = "/invalid/path/progress.json"
        
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 500)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)


if __name__ == '__main__':
    unittest.main()