"""
Unit tests for ProgressManager service
"""
import unittest
import tempfile
import os
import json
from datetime import datetime
from services.progress_manager import ProgressManager


class TestProgressManager(unittest.TestCase):
    """Test cases for ProgressManager class"""
    
    def setUp(self):
        """Set up test environment with temporary file"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, "test_progress.json")
        self.progress_manager = ProgressManager(self.test_file)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.test_dir)
    
    def test_initialization(self):
        """Test that ProgressManager initializes properly"""
        self.assertTrue(os.path.exists(self.test_file))
        data = self.progress_manager.get_progress()
        self.assertIsInstance(data, dict)
        self.assertIn('today_completed', data)
        self.assertIn('today_focus_time', data)
        self.assertIn('last_update', data)
        self.assertIn('total_completed', data)
        self.assertIn('total_focus_time', data)
    
    def test_get_progress(self):
        """Test getting progress data"""
        progress = self.progress_manager.get_progress()
        self.assertEqual(progress['today_completed'], 0)
        self.assertEqual(progress['today_focus_time'], 0)
        self.assertEqual(progress['total_completed'], 0)
        self.assertEqual(progress['total_focus_time'], 0)
        self.assertEqual(progress['last_update'], datetime.now().strftime("%Y-%m-%d"))
    
    def test_add_completed_session_default(self):
        """Test adding a completed session with default time"""
        result = self.progress_manager.add_completed_session()
        self.assertEqual(result['today_completed'], 1)
        self.assertEqual(result['today_focus_time'], 25)
        self.assertEqual(result['total_completed'], 1)
        self.assertEqual(result['total_focus_time'], 25)
    
    def test_add_completed_session_custom_time(self):
        """Test adding a completed session with custom time"""
        result = self.progress_manager.add_completed_session(30)
        self.assertEqual(result['today_completed'], 1)
        self.assertEqual(result['today_focus_time'], 30)
        self.assertEqual(result['total_completed'], 1)
        self.assertEqual(result['total_focus_time'], 30)
    
    def test_add_multiple_sessions(self):
        """Test adding multiple completed sessions"""
        self.progress_manager.add_completed_session(25)
        self.progress_manager.add_completed_session(30)
        result = self.progress_manager.add_completed_session(20)
        
        self.assertEqual(result['today_completed'], 3)
        self.assertEqual(result['today_focus_time'], 75)
        self.assertEqual(result['total_completed'], 3)
        self.assertEqual(result['total_focus_time'], 75)
    
    def test_reset_today_progress(self):
        """Test resetting today's progress"""
        # Add some progress
        self.progress_manager.add_completed_session(25)
        self.progress_manager.add_completed_session(30)
        
        # Reset today's progress
        result = self.progress_manager.reset_today_progress()
        
        self.assertEqual(result['today_completed'], 0)
        self.assertEqual(result['today_focus_time'], 0)
        # Total should remain unchanged
        self.assertEqual(result['total_completed'], 2)
        self.assertEqual(result['total_focus_time'], 55)
    
    def test_update_progress(self):
        """Test updating progress with custom data"""
        update_data = {
            'today_completed': 5,
            'today_focus_time': 125,
            'custom_field': 'test_value'
        }
        result = self.progress_manager.update_progress(update_data)
        
        self.assertEqual(result['today_completed'], 5)
        self.assertEqual(result['today_focus_time'], 125)
        self.assertEqual(result['custom_field'], 'test_value')
    
    def test_data_persistence(self):
        """Test that data persists across instances"""
        # Add data with first instance
        self.progress_manager.add_completed_session(25)
        
        # Create new instance with same file
        new_manager = ProgressManager(self.test_file)
        result = new_manager.get_progress()
        
        self.assertEqual(result['today_completed'], 1)
        self.assertEqual(result['today_focus_time'], 25)
    
    def test_file_corruption_recovery(self):
        """Test recovery from corrupted data file"""
        # Write invalid JSON to file
        with open(self.test_file, 'w') as f:
            f.write("invalid json content")
        
        # Should recover gracefully
        new_manager = ProgressManager(self.test_file)
        result = new_manager.get_progress()
        
        # Should have default values
        self.assertEqual(result['today_completed'], 0)
        self.assertEqual(result['today_focus_time'], 0)
    
    def test_daily_reset_logic(self):
        """Test that daily counters reset when date changes"""
        # Manually create data with yesterday's date
        yesterday_data = {
            "today_completed": 5,
            "today_focus_time": 125,
            "last_update": "2024-01-01",  # Old date
            "total_completed": 10,
            "total_focus_time": 250
        }
        
        with open(self.test_file, 'w') as f:
            json.dump(yesterday_data, f)
        
        # Create new manager - should reset daily counters
        new_manager = ProgressManager(self.test_file)
        result = new_manager.get_progress()
        
        # Daily counters should be reset
        self.assertEqual(result['today_completed'], 0)
        self.assertEqual(result['today_focus_time'], 0)
        # Totals should remain
        self.assertEqual(result['total_completed'], 10)
        self.assertEqual(result['total_focus_time'], 250)
        # Date should be updated to today
        self.assertEqual(result['last_update'], datetime.now().strftime("%Y-%m-%d"))


if __name__ == '__main__':
    unittest.main()