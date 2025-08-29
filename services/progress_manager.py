"""
Progress Manager Service for Pomodoro Timer
Handles progress data persistence and management
"""
import json
import os
from datetime import datetime
from typing import Dict, Any


class ProgressManager:
    """Manages progress data for the Pomodoro timer application"""
    
    def __init__(self, data_file: str = "data/progress.json"):
        """
        Initialize progress manager with data file path
        
        Args:
            data_file (str): Path to the progress data JSON file
        """
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self) -> None:
        """Ensure the data file and directory exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self._initialize_data_file()
    
    def _initialize_data_file(self) -> None:
        """Initialize the data file with default values"""
        default_data = {
            "today_completed": 0,
            "today_focus_time": 0,
            "last_update": datetime.now().strftime("%Y-%m-%d"),
            "total_completed": 0,
            "total_focus_time": 0
        }
        self._save_data(default_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load progress data from file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Reset daily counters if it's a new day
                today = datetime.now().strftime("%Y-%m-%d")
                if data.get("last_update") != today:
                    data["today_completed"] = 0
                    data["today_focus_time"] = 0
                    data["last_update"] = today
                    self._save_data(data)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            self._initialize_data_file()
            return self._load_data()
    
    def _save_data(self, data: Dict[str, Any]) -> None:
        """Save progress data to file"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data"""
        return self._load_data()
    
    def add_completed_session(self, focus_time_minutes: int = 25) -> Dict[str, Any]:
        """
        Add a completed Pomodoro session
        
        Args:
            focus_time_minutes (int): Minutes of focus time to add
            
        Returns:
            Dict[str, Any]: Updated progress data
        """
        data = self._load_data()
        data["today_completed"] += 1
        data["today_focus_time"] += focus_time_minutes
        data["total_completed"] += 1
        data["total_focus_time"] += focus_time_minutes
        data["last_update"] = datetime.now().strftime("%Y-%m-%d")
        self._save_data(data)
        return data
    
    def reset_today_progress(self) -> Dict[str, Any]:
        """
        Reset today's progress counters
        
        Returns:
            Dict[str, Any]: Updated progress data
        """
        data = self._load_data()
        data["today_completed"] = 0
        data["today_focus_time"] = 0
        data["last_update"] = datetime.now().strftime("%Y-%m-%d")
        self._save_data(data)
        return data
    
    def update_progress(self, progress_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update progress data with provided values
        
        Args:
            progress_data (Dict[str, Any]): Progress data to update
            
        Returns:
            Dict[str, Any]: Updated progress data
        """
        data = self._load_data()
        data.update(progress_data)
        data["last_update"] = datetime.now().strftime("%Y-%m-%d")
        self._save_data(data)
        return data