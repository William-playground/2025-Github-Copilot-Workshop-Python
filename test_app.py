import unittest
from app import create_app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Use testing configuration with dependency injection
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)
        self.assertIn('ポモドーロタイマー'.encode('utf-8'), response.data)

    def test_get_progress_api(self):
        response = self.client.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('completed_sessions', data)
        self.assertIn('total_focus_minutes', data)
        self.assertIn('today', data)

    def test_complete_session_api(self):
        # Test completing a session
        response = self.client.post('/api/progress', 
                                  json={'action': 'complete_session', 'duration_minutes': 25})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['completed_sessions'], 1)
        self.assertEqual(data['total_focus_minutes'], 25)

    def test_reset_progress_api(self):
        # First complete a session
        self.client.post('/api/progress', 
                        json={'action': 'complete_session', 'duration_minutes': 25})
        
        # Then reset
        response = self.client.post('/api/progress', json={'action': 'reset'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['completed_sessions'], 0)
        self.assertEqual(data['total_focus_minutes'], 0)

    def test_invalid_api_request(self):
        # Test invalid action
        response = self.client.post('/api/progress', json={'action': 'invalid'})
        self.assertEqual(response.status_code, 400)
        
        # Test no data
        response = self.client.post('/api/progress')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
