import unittest
from unittest.mock import Mock, patch
from app import create_app
from services.interfaces import ProgressManager


class MockProgressManager(ProgressManager):
    """Mock progress manager for testing dependency injection."""
    
    def __init__(self):
        self.daily_progress_called = False
        self.add_session_called = False
        self.reset_called = False
        self.progress_data = {
            "today": "2024-01-01",
            "completed_sessions": 0,
            "total_focus_minutes": 0,
            "last_updated": "2024-01-01T00:00:00"
        }
    
    def get_daily_progress(self):
        self.daily_progress_called = True
        return self.progress_data.copy()
    
    def add_completed_session(self, session_duration_minutes=25):
        self.add_session_called = True
        self.progress_data["completed_sessions"] += 1
        self.progress_data["total_focus_minutes"] += session_duration_minutes
        return self.progress_data.copy()
    
    def reset_daily_progress(self):
        self.reset_called = True
        self.progress_data["completed_sessions"] = 0
        self.progress_data["total_focus_minutes"] = 0
        return self.progress_data.copy()


class TestAppWithDependencyInjection(unittest.TestCase):
    
    def setUp(self):
        self.mock_progress_manager = MockProgressManager()
        self.app = create_app('testing', self.mock_progress_manager)
        self.client = self.app.test_client()
    
    def test_dependency_injection_works(self):
        """Test that dependency injection is working properly."""
        self.assertIs(self.app.progress_manager, self.mock_progress_manager)
    
    def test_get_progress_uses_injected_manager(self):
        """Test that GET /api/progress uses the injected progress manager."""
        response = self.client.get('/api/progress')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.mock_progress_manager.daily_progress_called)
    
    def test_complete_session_uses_injected_manager(self):
        """Test that POST /api/progress uses the injected progress manager."""
        response = self.client.post('/api/progress', 
                                  json={'action': 'complete_session', 'duration_minutes': 25})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.mock_progress_manager.add_session_called)
        
        data = response.get_json()
        self.assertEqual(data['completed_sessions'], 1)
        self.assertEqual(data['total_focus_minutes'], 25)
    
    def test_reset_uses_injected_manager(self):
        """Test that reset action uses the injected progress manager."""
        response = self.client.post('/api/progress', json={'action': 'reset'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.mock_progress_manager.reset_called)
        
        data = response.get_json()
        self.assertEqual(data['completed_sessions'], 0)
        self.assertEqual(data['total_focus_minutes'], 0)


class TestAppFactory(unittest.TestCase):
    
    def test_create_app_with_default_config(self):
        """Test creating app with default configuration."""
        app = create_app()
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(hasattr(app, 'progress_manager'))
    
    def test_create_app_with_testing_config(self):
        """Test creating app with testing configuration."""
        app = create_app('testing')
        self.assertTrue(app.config['TESTING'])
        self.assertTrue(hasattr(app, 'progress_manager'))
    
    def test_create_app_with_custom_progress_manager(self):
        """Test creating app with custom progress manager."""
        mock_manager = MockProgressManager()
        app = create_app('testing', mock_manager)
        self.assertIs(app.progress_manager, mock_manager)


if __name__ == '__main__':
    unittest.main()