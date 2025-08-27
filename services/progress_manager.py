"""
Progress Manager for Pomodoro Timer
Handles loading and saving progress data to JSON file
"""
import json
import os
from datetime import datetime
from typing import Dict, Any

class ProgressManager:
    def __init__(self, data_file: str = "data/progress.json"):
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """Ensure the data file and directory exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            # Initialize with default data
            default_data = {
                "completed_sessions": 0,
                "total_focus_time": 0,  # in minutes
                "last_updated": datetime.now().isoformat()
            }
            self._save_data(default_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load progress data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default data if file doesn't exist or is corrupted
            return {
                "completed_sessions": 0,
                "total_focus_time": 0,
                "last_updated": datetime.now().isoformat()
            }
    
    def _save_data(self, data: Dict[str, Any]):
        """Save progress data to JSON file"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data"""
        return self._load_data()
    
    def update_progress(self, completed_sessions: int = None, total_focus_time: int = None) -> Dict[str, Any]:
        """Update progress data and return the updated data"""
        data = self._load_data()
        
        if completed_sessions is not None:
            data["completed_sessions"] = completed_sessions
        
        if total_focus_time is not None:
            data["total_focus_time"] = total_focus_time
        
        self._save_data(data)
        return data
    
    def add_completed_session(self, session_duration: int = 25) -> Dict[str, Any]:
        """Add a completed session and update focus time"""
        data = self._load_data()
        data["completed_sessions"] += 1
        data["total_focus_time"] += session_duration
        self._save_data(data)
        return data
    
    def reset_progress(self) -> Dict[str, Any]:
        """Reset progress to default values"""
        data = {
            "completed_sessions": 0,
            "total_focus_time": 0,
            "last_updated": datetime.now().isoformat()
        }
        self._save_data(data)
        return data