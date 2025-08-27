"""Progress manager for Pomodoro timer application."""

import json
import os
from datetime import datetime, date
from typing import Dict, Any, Optional


class ProgressManager:
    """Manages progress data for the Pomodoro timer."""
    
    def __init__(self, data_file: str = "data/progress.json"):
        """Initialize the progress manager.
        
        Args:
            data_file: Path to the JSON file for storing progress data
        """
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self) -> None:
        """Ensure the data file and directory exist."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self._save_data({})
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from the JSON file.
        
        Returns:
            Dictionary containing progress data
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save data to the JSON file.
        
        Args:
            data: Dictionary containing progress data to save
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_today_progress(self) -> Dict[str, Any]:
        """Get today's progress data.
        
        Returns:
            Dictionary with today's completed sessions and focus time
        """
        data = self._load_data()
        today = date.today().isoformat()
        
        today_data = data.get(today, {})
        return {
            "date": today,
            "completed_sessions": today_data.get("completed_sessions", 0),
            "focus_time": today_data.get("focus_time", 0)  # in minutes
        }
    
    def add_completed_session(self, session_duration: int = 25) -> Dict[str, Any]:
        """Add a completed Pomodoro session.
        
        Args:
            session_duration: Duration of the session in minutes (default: 25)
            
        Returns:
            Updated progress data for today
        """
        data = self._load_data()
        today = date.today().isoformat()
        
        if today not in data:
            data[today] = {"completed_sessions": 0, "focus_time": 0}
        
        data[today]["completed_sessions"] += 1
        data[today]["focus_time"] += session_duration
        
        self._save_data(data)
        return self.get_today_progress()
    
    def get_all_progress(self) -> Dict[str, Any]:
        """Get all progress data.
        
        Returns:
            Dictionary containing all progress data
        """
        return self._load_data()
    
    def reset_today_progress(self) -> Dict[str, Any]:
        """Reset today's progress data.
        
        Returns:
            Reset progress data for today
        """
        data = self._load_data()
        today = date.today().isoformat()
        data[today] = {"completed_sessions": 0, "focus_time": 0}
        self._save_data(data)
        return self.get_today_progress()