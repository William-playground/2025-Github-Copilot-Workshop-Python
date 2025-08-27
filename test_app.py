import unittest
import json
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<html', response.data)
    
    def test_get_progress(self):
        """Test the progress API endpoint"""
        response = self.app.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('total_xp', data)
        self.assertIn('level', data)
        self.assertIn('completed_pomodoros', data)
        self.assertIn('current_streak', data)
    
    def test_complete_pomodoro(self):
        """Test completing a Pomodoro via API"""
        # Get initial progress
        initial_response = self.app.get('/api/progress')
        initial_data = json.loads(initial_response.data)
        initial_xp = initial_data['total_xp']
        
        response = self.app.post('/api/progress/complete',
                                json={'focus_minutes': 25},
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('total_xp', data)
        self.assertIn('level', data)
        self.assertIn('new_achievements', data)
        self.assertEqual(data['total_xp'], initial_xp + 25)  # Should gain 25 XP
    
    def test_get_statistics(self):
        """Test the statistics API endpoint"""
        response = self.app.get('/api/statistics?period=week')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('daily_data', data)
        self.assertIn('total_completions', data)
        self.assertIn('period', data)
        self.assertEqual(data['period'], 'week')
    
    def test_get_achievements(self):
        """Test the achievements API endpoint"""
        response = self.app.get('/api/achievements')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check achievement structure
        achievement = data[0]
        self.assertIn('id', achievement)
        self.assertIn('name', achievement)
        self.assertIn('description', achievement)
        self.assertIn('unlocked', achievement)

if __name__ == '__main__':
    unittest.main()
