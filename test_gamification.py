"""
Tests for the gamification manager
"""
import unittest
import os
import tempfile
from services.gamification_manager import GamificationManager, UserProgress, Achievement


class TestGamificationManager(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.manager = GamificationManager(self.temp_file.name)
    
    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_initial_progress(self):
        """Test initial progress state"""
        progress = self.manager.get_progress()
        self.assertEqual(progress['total_xp'], 0)
        self.assertEqual(progress['level'], 1)
        self.assertEqual(progress['completed_pomodoros'], 0)
        self.assertEqual(progress['current_streak'], 0)
    
    def test_complete_pomodoro(self):
        """Test completing a Pomodoro"""
        result = self.manager.complete_pomodoro(25)
        
        self.assertEqual(result['total_xp'], 25)
        self.assertEqual(result['level'], 1)
        self.assertEqual(result['completed_pomodoros'], 1)
        self.assertEqual(result['current_streak'], 1)
        self.assertFalse(result['level_up'])
        
        # Check for first timer achievement
        self.assertEqual(len(result['new_achievements']), 1)
        self.assertEqual(result['new_achievements'][0].id, 'first_timer')
    
    def test_level_up(self):
        """Test leveling up"""
        # Complete 4 Pomodoros (4 * 25 = 100 XP = level up)
        for i in range(4):
            result = self.manager.complete_pomodoro(25)
        
        self.assertEqual(result['total_xp'], 100)
        self.assertEqual(result['level'], 2)
        self.assertTrue(result['level_up'])
        self.assertEqual(result['xp_to_next_level'], 100)
    
    def test_achievements_unlock(self):
        """Test achievement unlocking"""
        # Test first timer
        result = self.manager.complete_pomodoro()
        first_timer_unlocked = any(ach.id == 'first_timer' for ach in result['new_achievements'])
        self.assertTrue(first_timer_unlocked)
        
        # Test level 5 achievement (need 400 XP total)
        for i in range(15):  # 16 total * 25 = 400 XP = level 5
            self.manager.complete_pomodoro()
        
        progress = self.manager.get_progress()
        level_5_unlocked = any(ach['id'] == 'level_5' for ach in progress['achievements'])
        self.assertTrue(level_5_unlocked)
    
    def test_statistics(self):
        """Test statistics calculation"""
        # Complete a few Pomodoros
        for i in range(3):
            self.manager.complete_pomodoro(25)
        
        stats = self.manager.get_statistics('week')
        self.assertEqual(stats['total_completions'], 3)
        self.assertEqual(stats['total_focus_time'], 75)
        self.assertGreater(stats['average_daily'], 0)
    
    def test_persistence(self):
        """Test data persistence"""
        # Complete a Pomodoro
        self.manager.complete_pomodoro(25)
        
        # Create new manager instance with same file
        new_manager = GamificationManager(self.temp_file.name)
        progress = new_manager.get_progress()
        
        self.assertEqual(progress['total_xp'], 25)
        self.assertEqual(progress['completed_pomodoros'], 1)
        self.assertEqual(progress['achievements_count'], 1)  # First timer should be unlocked


if __name__ == '__main__':
    unittest.main()