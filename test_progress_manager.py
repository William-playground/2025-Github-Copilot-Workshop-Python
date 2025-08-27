import unittest
import os
import tempfile
import json
from services.progress_manager import ProgressManager

class ProgressManagerTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, "test_progress.json")
        self.progress_manager = ProgressManager(self.test_data_file)

    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        os.rmdir(self.temp_dir)

    def test_initial_data_creation(self):
        """Test that initial data file is created with default values"""
        self.assertTrue(os.path.exists(self.test_data_file))
        
        data = self.progress_manager.get_progress()
        self.assertEqual(data['completed_sessions'], 0)
        self.assertEqual(data['total_focus_time'], 0)
        self.assertIn('last_updated', data)

    def test_update_progress(self):
        """Test updating progress values"""
        updated_data = self.progress_manager.update_progress(
            completed_sessions=3, 
            total_focus_time=75
        )
        
        self.assertEqual(updated_data['completed_sessions'], 3)
        self.assertEqual(updated_data['total_focus_time'], 75)
        
        # Verify persistence
        data = self.progress_manager.get_progress()
        self.assertEqual(data['completed_sessions'], 3)
        self.assertEqual(data['total_focus_time'], 75)

    def test_add_completed_session(self):
        """Test adding completed sessions"""
        # Add first session
        data = self.progress_manager.add_completed_session(25)
        self.assertEqual(data['completed_sessions'], 1)
        self.assertEqual(data['total_focus_time'], 25)
        
        # Add second session with different duration
        data = self.progress_manager.add_completed_session(30)
        self.assertEqual(data['completed_sessions'], 2)
        self.assertEqual(data['total_focus_time'], 55)

    def test_reset_progress(self):
        """Test resetting progress"""
        # First add some data
        self.progress_manager.update_progress(
            completed_sessions=5, 
            total_focus_time=125
        )
        
        # Then reset
        data = self.progress_manager.reset_progress()
        self.assertEqual(data['completed_sessions'], 0)
        self.assertEqual(data['total_focus_time'], 0)

    def test_data_persistence_across_instances(self):
        """Test that data persists across different ProgressManager instances"""
        # Update data with first instance
        self.progress_manager.update_progress(
            completed_sessions=2, 
            total_focus_time=50
        )
        
        # Create new instance with same file
        new_manager = ProgressManager(self.test_data_file)
        data = new_manager.get_progress()
        
        self.assertEqual(data['completed_sessions'], 2)
        self.assertEqual(data['total_focus_time'], 50)

if __name__ == '__main__':
    unittest.main()