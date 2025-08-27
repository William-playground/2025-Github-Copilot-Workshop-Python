import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from services.progress_manager import PomodoroProgressManager
from services.repositories import InMemoryProgressRepository
from services.interfaces import ProgressRepository


class MockProgressRepository(ProgressRepository):
    """Mock implementation for testing."""
    
    def __init__(self):
        self.data = {
            "today": "2024-01-01",
            "completed_sessions": 0,
            "total_focus_minutes": 0,
            "last_updated": "2024-01-01T00:00:00"
        }
        self.save_called = False
    
    def get_progress(self):
        return self.data.copy()
    
    def save_progress(self, progress_data):
        self.data = progress_data.copy()
        self.save_called = True
        return True


class TestPomodoroProgressManager(unittest.TestCase):
    
    def setUp(self):
        self.mock_repo = MockProgressRepository()
        self.manager = PomodoroProgressManager(self.mock_repo)
    
    def test_get_daily_progress_same_day(self):
        """Test getting progress for the same day."""
        with patch('services.progress_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-01-01"
            
            progress = self.manager.get_daily_progress()
            self.assertEqual(progress['completed_sessions'], 0)
            self.assertEqual(progress['total_focus_minutes'], 0)
            self.assertFalse(self.mock_repo.save_called)
    
    def test_get_daily_progress_new_day(self):
        """Test getting progress for a new day (should reset)."""
        with patch('services.progress_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-01-02"
            mock_datetime.now.return_value.isoformat.return_value = "2024-01-02T00:00:00"
            
            progress = self.manager.get_daily_progress()
            self.assertEqual(progress['today'], "2024-01-02")
            self.assertEqual(progress['completed_sessions'], 0)
            self.assertEqual(progress['total_focus_minutes'], 0)
            self.assertTrue(self.mock_repo.save_called)
    
    def test_add_completed_session(self):
        """Test adding a completed session."""
        with patch('services.progress_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-01-01"
            mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T12:00:00"
            
            progress = self.manager.add_completed_session(25)
            self.assertEqual(progress['completed_sessions'], 1)
            self.assertEqual(progress['total_focus_minutes'], 25)
            self.assertEqual(progress['last_updated'], "2024-01-01T12:00:00")
            self.assertTrue(self.mock_repo.save_called)
    
    def test_add_completed_session_custom_duration(self):
        """Test adding a completed session with custom duration."""
        with patch('services.progress_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-01-01"
            mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T12:00:00"
            
            progress = self.manager.add_completed_session(30)
            self.assertEqual(progress['completed_sessions'], 1)
            self.assertEqual(progress['total_focus_minutes'], 30)
    
    def test_reset_daily_progress(self):
        """Test resetting daily progress."""
        # First add some progress
        with patch('services.progress_manager.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-01-01"
            mock_datetime.now.return_value.isoformat.return_value = "2024-01-01T12:00:00"
            
            self.manager.add_completed_session(25)
            
            # Then reset
            progress = self.manager.reset_daily_progress()
            self.assertEqual(progress['completed_sessions'], 0)
            self.assertEqual(progress['total_focus_minutes'], 0)
            self.assertEqual(progress['today'], "2024-01-01")


class TestInMemoryProgressRepository(unittest.TestCase):
    
    def setUp(self):
        self.repo = InMemoryProgressRepository()
    
    def test_get_progress_default(self):
        """Test getting default progress data."""
        progress = self.repo.get_progress()
        self.assertIn('completed_sessions', progress)
        self.assertIn('total_focus_minutes', progress)
        self.assertIn('today', progress)
        self.assertEqual(progress['completed_sessions'], 0)
    
    def test_save_and_get_progress(self):
        """Test saving and retrieving progress data."""
        test_data = {
            "today": "2024-01-01",
            "completed_sessions": 5,
            "total_focus_minutes": 125,
            "last_updated": "2024-01-01T12:00:00"
        }
        
        success = self.repo.save_progress(test_data)
        self.assertTrue(success)
        
        retrieved = self.repo.get_progress()
        self.assertEqual(retrieved, test_data)


if __name__ == '__main__':
    unittest.main()