import json
import os
from datetime import datetime, date
from typing import Dict, Any


class ProgressManager:
    """進捗データ管理クラス"""
    
    def __init__(self, data_file_path: str = "data/progress.json"):
        self.data_file_path = data_file_path
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        """データファイルが存在しない場合は作成"""
        os.makedirs(os.path.dirname(self.data_file_path), exist_ok=True)
        if not os.path.exists(self.data_file_path):
            initial_data = {
                "daily_progress": {},
                "total_sessions": 0,
                "total_focus_minutes": 0
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """進捗データをファイルから読み込み"""
        try:
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # ファイルが存在しないか破損している場合は初期データを返す
            return {
                "daily_progress": {},
                "total_sessions": 0,
                "total_focus_minutes": 0
            }
    
    def _save_data(self, data: Dict[str, Any]):
        """進捗データをファイルに保存"""
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_today_progress(self) -> Dict[str, Any]:
        """今日の進捗データを取得"""
        data = self._load_data()
        today_str = date.today().isoformat()
        
        daily_data = data["daily_progress"].get(today_str, {
            "completed_sessions": 0,
            "focus_minutes": 0
        })
        
        return {
            "date": today_str,
            "completed_sessions": daily_data["completed_sessions"],
            "focus_minutes": daily_data["focus_minutes"]
        }
    
    def add_completed_session(self, focus_minutes: int = 25):
        """完了したセッションを記録"""
        data = self._load_data()
        today_str = date.today().isoformat()
        
        # 今日のデータがない場合は初期化
        if today_str not in data["daily_progress"]:
            data["daily_progress"][today_str] = {
                "completed_sessions": 0,
                "focus_minutes": 0
            }
        
        # 今日のデータを更新
        data["daily_progress"][today_str]["completed_sessions"] += 1
        data["daily_progress"][today_str]["focus_minutes"] += focus_minutes
        
        # 総計を更新
        data["total_sessions"] += 1
        data["total_focus_minutes"] += focus_minutes
        
        self._save_data(data)
        return self.get_today_progress()
    
    def get_all_progress(self) -> Dict[str, Any]:
        """全ての進捗データを取得"""
        return self._load_data()