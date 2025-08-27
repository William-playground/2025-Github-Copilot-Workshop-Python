from typing import Dict, Any
from datetime import datetime
from .interfaces import ProgressManager, ProgressRepository


class PomodoroProgressManager(ProgressManager):
    """Concrete implementation of ProgressManager for pomodoro sessions."""
    
    def __init__(self, repository: ProgressRepository):
        self.repository = repository
    
    def get_daily_progress(self) -> Dict[str, Any]:
        """Get today's progress statistics."""
        progress = self.repository.get_progress()
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Reset progress if it's a new day
        if progress.get("today") != today:
            progress = self._reset_for_new_day(today)
            self.repository.save_progress(progress)
        
        return progress
    
    def add_completed_session(self, session_duration_minutes: int = 25) -> Dict[str, Any]:
        """Add a completed pomodoro session."""
        progress = self.get_daily_progress()
        
        progress["completed_sessions"] += 1
        progress["total_focus_minutes"] += session_duration_minutes
        progress["last_updated"] = datetime.now().isoformat()
        
        self.repository.save_progress(progress)
        return progress
    
    def reset_daily_progress(self) -> Dict[str, Any]:
        """Reset today's progress."""
        today = datetime.now().strftime("%Y-%m-%d")
        progress = self._reset_for_new_day(today)
        self.repository.save_progress(progress)
        return progress
    
    def _reset_for_new_day(self, today: str) -> Dict[str, Any]:
        """Reset progress for a new day."""
        return {
            "today": today,
            "completed_sessions": 0,
            "total_focus_minutes": 0,
            "last_updated": datetime.now().isoformat()
        }