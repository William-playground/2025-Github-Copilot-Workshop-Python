import json
import os
from typing import Dict, Any
from datetime import datetime
from .interfaces import ProgressRepository


class FileProgressRepository(ProgressRepository):
    """File-based implementation of ProgressRepository."""
    
    def __init__(self, file_path: str = "data/progress.json"):
        self.file_path = file_path
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data from file."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            return self._get_default_progress()
        except (json.JSONDecodeError, IOError):
            return self._get_default_progress()
    
    def save_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Save progress data to file."""
        try:
            self._ensure_data_directory()
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(progress_data, file, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def _get_default_progress(self) -> Dict[str, Any]:
        """Get default progress structure."""
        return {
            "today": datetime.now().strftime("%Y-%m-%d"),
            "completed_sessions": 0,
            "total_focus_minutes": 0,
            "last_updated": datetime.now().isoformat()
        }


class InMemoryProgressRepository(ProgressRepository):
    """In-memory implementation of ProgressRepository for testing."""
    
    def __init__(self):
        self._data = {
            "today": datetime.now().strftime("%Y-%m-%d"),
            "completed_sessions": 0,
            "total_focus_minutes": 0,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_progress(self) -> Dict[str, Any]:
        """Get current progress data from memory."""
        return self._data.copy()
    
    def save_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Save progress data to memory."""
        self._data = progress_data.copy()
        return True