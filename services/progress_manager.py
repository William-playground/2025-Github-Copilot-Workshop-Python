import json
import os
from datetime import datetime, date
from typing import Dict, Any


class ProgressManager:
    """Manages Pomodoro progress data storage and retrieval."""
    
    def __init__(self, data_file: str = "data/progress.json"):
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self) -> None:
        """Ensure the data file exists with proper structure."""
        if not os.path.exists(self.data_file):
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            initial_data = {
                "today": date.today().isoformat(),
                "completed_sessions": 0,
                "total_focus_time": 0,
                "last_session_date": None
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(initial_data, f, indent=2, ensure_ascii=False)
    
    def _reset_daily_data_if_needed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Reset daily data if it's a new day."""
        today = date.today().isoformat()
        if data.get("today") != today:
            data["today"] = today
            data["completed_sessions"] = 0
            data["total_focus_time"] = 0
        return data
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data = self._reset_daily_data_if_needed(data)
            
            # Save updated data if the date was reset
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            # If file is corrupted or missing, recreate it
            self._ensure_data_file_exists()
            # Return the initial data directly to avoid recursion
            return {
                "today": date.today().isoformat(),
                "completed_sessions": 0,
                "total_focus_time": 0,
                "last_session_date": None
            }
    
    def complete_session(self, focus_time_minutes: int = 25) -> Dict[str, Any]:
        """Record a completed Pomodoro session."""
        data = self.get_progress()
        data["completed_sessions"] += 1
        data["total_focus_time"] += focus_time_minutes
        data["last_session_date"] = datetime.now().isoformat()
        
        # Save updated data
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return data
    
    def update_progress(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update progress data with provided updates."""
        data = self.get_progress()
        
        # Only allow updates to specific fields
        allowed_fields = ["completed_sessions", "total_focus_time"]
        for field in allowed_fields:
            if field in updates:
                data[field] = updates[field]
        
        # Always update the today field to current date
        data["today"] = date.today().isoformat()
        
        # Save updated data
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return data