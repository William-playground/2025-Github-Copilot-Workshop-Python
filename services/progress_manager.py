"""
Progress Manager Service
Handles pomodoro progress data storage and retrieval
"""
import json
import os
from datetime import datetime, date
from typing import Dict, Any


class ProgressManager:
    def __init__(self, data_file: str = "data/progress.json"):
        self.data_file = data_file
        self._ensure_data_file()
    
    def _ensure_data_file(self):
        """Ensure the data file exists with default structure"""
        if not os.path.exists(self.data_file):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            # Create initial data structure
            initial_data = {
                "total_sessions": 0,
                "total_focus_time": 0,
                "daily_progress": {}
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load progress data from JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default data if file doesn't exist or is corrupted
            return {
                "total_sessions": 0,
                "total_focus_time": 0,
                "daily_progress": {}
            }
    
    def _save_data(self, data: Dict[str, Any]):
        """Save progress data to JSON file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data"""
        data = self._load_data()
        today = date.today().isoformat()
        
        # Get today's progress
        today_progress = data.get("daily_progress", {}).get(today, {
            "completed_sessions": 0,
            "focus_time": 0
        })
        
        return {
            "today": {
                "completed_sessions": today_progress["completed_sessions"],
                "focus_time": today_progress["focus_time"]
            },
            "total": {
                "sessions": data.get("total_sessions", 0),
                "focus_time": data.get("total_focus_time", 0)
            }
        }
    
    def add_completed_session(self, focus_time_minutes: int = 25):
        """Record a completed pomodoro session"""
        data = self._load_data()
        today = date.today().isoformat()
        
        # Initialize today's data if not exists
        if "daily_progress" not in data:
            data["daily_progress"] = {}
        
        if today not in data["daily_progress"]:
            data["daily_progress"][today] = {
                "completed_sessions": 0,
                "focus_time": 0
            }
        
        # Update today's progress
        data["daily_progress"][today]["completed_sessions"] += 1
        data["daily_progress"][today]["focus_time"] += focus_time_minutes
        
        # Update totals
        data["total_sessions"] = data.get("total_sessions", 0) + 1
        data["total_focus_time"] = data.get("total_focus_time", 0) + focus_time_minutes
        
        self._save_data(data)
        
        return self.get_progress()