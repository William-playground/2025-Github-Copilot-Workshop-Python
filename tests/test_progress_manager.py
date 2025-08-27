import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import tempfile
import shutil
from datetime import date
from services.progress_manager import ProgressManager


class TestProgressManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_progress.json")
        self.progress_manager = ProgressManager(self.test_file)
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_initialization(self):
        """Test that ProgressManager initializes correctly."""
        self.assertTrue(os.path.exists(self.test_file))
        progress = self.progress_manager.get_today_progress()
        self.assertIn('date', progress)
        self.assertIn('completed_sessions', progress)
        self.assertIn('focus_time', progress)
    
    def test_get_today_progress_initial(self):
        """Test getting today's progress when no data exists."""
        progress = self.progress_manager.get_today_progress()
        self.assertEqual(progress['completed_sessions'], 0)
        self.assertEqual(progress['focus_time'], 0)
        self.assertEqual(progress['date'], date.today().isoformat())
    
    def test_add_completed_session_default(self):
        """Test adding a completed session with default duration."""
        progress = self.progress_manager.add_completed_session()
        self.assertEqual(progress['completed_sessions'], 1)
        self.assertEqual(progress['focus_time'], 25)
    
    def test_add_completed_session_custom_duration(self):
        """Test adding a completed session with custom duration."""
        progress = self.progress_manager.add_completed_session(30)
        self.assertEqual(progress['completed_sessions'], 1)
        self.assertEqual(progress['focus_time'], 30)
    
    def test_multiple_sessions(self):
        """Test adding multiple sessions."""
        self.progress_manager.add_completed_session(25)
        self.progress_manager.add_completed_session(15)
        progress = self.progress_manager.get_today_progress()
        self.assertEqual(progress['completed_sessions'], 2)
        self.assertEqual(progress['focus_time'], 40)
    
    def test_reset_today_progress(self):
        """Test resetting today's progress."""
        # Add some sessions first
        self.progress_manager.add_completed_session(25)
        self.progress_manager.add_completed_session(25)
        
        # Reset progress
        progress = self.progress_manager.reset_today_progress()
        self.assertEqual(progress['completed_sessions'], 0)
        self.assertEqual(progress['focus_time'], 0)
    
    def test_get_all_progress(self):
        """Test getting all progress data."""
        self.progress_manager.add_completed_session(25)
        all_progress = self.progress_manager.get_all_progress()
        self.assertIsInstance(all_progress, dict)
        today = date.today().isoformat()
        self.assertIn(today, all_progress)
        self.assertEqual(all_progress[today]['completed_sessions'], 1)
    
    def test_data_persistence(self):
        """Test that data persists across ProgressManager instances."""
        # Add data with first instance
        self.progress_manager.add_completed_session(25)
        
        # Create new instance with same file
        new_manager = ProgressManager(self.test_file)
        progress = new_manager.get_today_progress()
        self.assertEqual(progress['completed_sessions'], 1)
        self.assertEqual(progress['focus_time'], 25)
    
    def test_invalid_file_recovery(self):
        """Test recovery from corrupted data file."""
        # Write invalid JSON to file
        with open(self.test_file, 'w') as f:
            f.write("invalid json content")
        
        # Should still work with empty data
        manager = ProgressManager(self.test_file)
        progress = manager.get_today_progress()
        self.assertEqual(progress['completed_sessions'], 0)
        self.assertEqual(progress['focus_time'], 0)


if __name__ == '__main__':
    unittest.main()