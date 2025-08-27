from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class ProgressRepository(ABC):
    """Abstract interface for progress data storage."""
    
    @abstractmethod
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data."""
        pass
    
    @abstractmethod
    def save_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Save progress data. Returns True if successful."""
        pass


class ProgressManager(ABC):
    """Abstract interface for progress management logic."""
    
    @abstractmethod
    def get_daily_progress(self) -> Dict[str, Any]:
        """Get today's progress statistics."""
        pass
    
    @abstractmethod
    def add_completed_session(self, session_duration_minutes: int = 25) -> Dict[str, Any]:
        """Add a completed pomodoro session. Returns updated progress."""
        pass
    
    @abstractmethod
    def reset_daily_progress(self) -> Dict[str, Any]:
        """Reset today's progress. Returns empty progress."""
        pass