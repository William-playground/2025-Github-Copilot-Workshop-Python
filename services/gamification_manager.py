"""
Gamification Manager for Pomodoro Timer
Handles XP, levels, badges, streaks, and statistics
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class Achievement:
    """Achievement/Badge data structure"""
    id: str
    name: str
    description: str
    icon: str
    unlocked_at: Optional[str] = None
    unlocked: bool = False


@dataclass
class UserProgress:
    """User progress and gamification data"""
    total_xp: int = 0
    level: int = 1
    completed_pomodoros: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_completion_date: Optional[str] = None
    achievements: List[Achievement] = None
    daily_stats: Dict[str, int] = None  # date -> completed count
    focus_time_minutes: int = 0
    
    def __post_init__(self):
        if self.achievements is None:
            self.achievements = []
        if self.daily_stats is None:
            self.daily_stats = {}


class GamificationManager:
    """Manages all gamification aspects of the Pomodoro timer"""
    
    def __init__(self, data_file: str = "data/progress.json"):
        self.data_file = data_file
        self.xp_per_pomodoro = 25
        self.xp_per_level = 100
        self.achievements_definitions = self._initialize_achievements()
        self.progress = self._load_progress()
    
    def _initialize_achievements(self) -> List[Achievement]:
        """Initialize all available achievements"""
        return [
            Achievement(
                id="first_timer",
                name="First Timer",
                description="Complete your first Pomodoro!",
                icon="🍅"
            ),
            Achievement(
                id="streak_3",
                name="Three Days Strong",
                description="Complete Pomodoros for 3 consecutive days",
                icon="🔥"
            ),
            Achievement(
                id="weekly_warrior",
                name="Weekly Warrior",
                description="Complete 10 Pomodoros in one week",
                icon="⚔️"
            ),
            Achievement(
                id="level_5",
                name="Rising Star",
                description="Reach level 5",
                icon="⭐"
            ),
            Achievement(
                id="focus_master",
                name="Focus Master",
                description="Accumulate 500 minutes of focus time",
                icon="🧠"
            ),
            Achievement(
                id="streak_7",
                name="Week Warrior",
                description="Complete Pomodoros for 7 consecutive days",
                icon="🏆"
            ),
            Achievement(
                id="century",
                name="Century Club",
                description="Complete 100 Pomodoros",
                icon="💯"
            )
        ]
    
    def _load_progress(self) -> UserProgress:
        """Load user progress from file"""
        if not os.path.exists(self.data_file):
            return UserProgress(achievements=self.achievements_definitions.copy())
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                
            # Convert achievements list back to Achievement objects
            achievements = []
            for ach_data in data.get('achievements', []):
                achievement = Achievement(**ach_data)
                achievements.append(achievement)
            
            # Update with new achievements if any
            existing_ids = {ach.id for ach in achievements}
            for new_ach in self.achievements_definitions:
                if new_ach.id not in existing_ids:
                    achievements.append(new_ach)
            
            data['achievements'] = achievements
            return UserProgress(**data)
            
        except (json.JSONDecodeError, KeyError, TypeError):
            # If file is corrupted, start fresh
            return UserProgress(achievements=self.achievements_definitions.copy())
    
    def _save_progress(self):
        """Save user progress to file"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        # Convert to dict, handling Achievement objects
        data = asdict(self.progress)
        data['achievements'] = [asdict(ach) for ach in self.progress.achievements]
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def complete_pomodoro(self, focus_minutes: int = 25) -> Dict:
        """
        Record a completed Pomodoro and update gamification data
        Returns updated progress and any new achievements
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Update basic stats
        old_level = self.progress.level
        self.progress.completed_pomodoros += 1
        self.progress.total_xp += self.xp_per_pomodoro
        self.progress.focus_time_minutes += focus_minutes
        
        # Calculate new level
        self.progress.level = (self.progress.total_xp // self.xp_per_level) + 1
        
        # Update daily stats
        self.progress.daily_stats[today] = self.progress.daily_stats.get(today, 0) + 1
        
        # Update streak
        self._update_streak(today)
        
        # Check for new achievements
        new_achievements = self._check_achievements()
        
        # Save progress
        self._save_progress()
        
        return {
            'total_xp': self.progress.total_xp,
            'level': self.progress.level,
            'level_up': self.progress.level > old_level,
            'completed_pomodoros': self.progress.completed_pomodoros,
            'current_streak': self.progress.current_streak,
            'new_achievements': new_achievements,
            'xp_to_next_level': self.xp_per_level - (self.progress.total_xp % self.xp_per_level)
        }
    
    def _update_streak(self, today: str):
        """Update the current streak based on today's completion"""
        today_date = datetime.strptime(today, "%Y-%m-%d")
        
        if self.progress.last_completion_date:
            last_date = datetime.strptime(self.progress.last_completion_date, "%Y-%m-%d")
            days_diff = (today_date - last_date).days
            
            if days_diff == 1:
                # Consecutive day
                self.progress.current_streak += 1
            elif days_diff == 0:
                # Same day, streak unchanged
                pass
            else:
                # Streak broken
                self.progress.current_streak = 1
        else:
            # First ever completion
            self.progress.current_streak = 1
        
        # Update longest streak
        if self.progress.current_streak > self.progress.longest_streak:
            self.progress.longest_streak = self.progress.current_streak
        
        self.progress.last_completion_date = today
    
    def _check_achievements(self) -> List[Achievement]:
        """Check and unlock new achievements"""
        new_achievements = []
        
        for achievement in self.progress.achievements:
            if achievement.unlocked:
                continue
                
            should_unlock = False
            
            # Check achievement conditions
            if achievement.id == "first_timer" and self.progress.completed_pomodoros >= 1:
                should_unlock = True
            elif achievement.id == "streak_3" and self.progress.current_streak >= 3:
                should_unlock = True
            elif achievement.id == "weekly_warrior" and self._get_weekly_completions() >= 10:
                should_unlock = True
            elif achievement.id == "level_5" and self.progress.level >= 5:
                should_unlock = True
            elif achievement.id == "focus_master" and self.progress.focus_time_minutes >= 500:
                should_unlock = True
            elif achievement.id == "streak_7" and self.progress.current_streak >= 7:
                should_unlock = True
            elif achievement.id == "century" and self.progress.completed_pomodoros >= 100:
                should_unlock = True
            
            if should_unlock:
                achievement.unlocked = True
                achievement.unlocked_at = datetime.now().isoformat()
                new_achievements.append(achievement)
        
        return new_achievements
    
    def _get_weekly_completions(self) -> int:
        """Get number of completions in the current week"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        count = 0
        for i in range(7):
            date_str = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            count += self.progress.daily_stats.get(date_str, 0)
        
        return count
    
    def get_progress(self) -> Dict:
        """Get current progress data"""
        return {
            'total_xp': self.progress.total_xp,
            'level': self.progress.level,
            'completed_pomodoros': self.progress.completed_pomodoros,
            'current_streak': self.progress.current_streak,
            'longest_streak': self.progress.longest_streak,
            'focus_time_minutes': self.progress.focus_time_minutes,
            'xp_to_next_level': self.xp_per_level - (self.progress.total_xp % self.xp_per_level),
            'xp_progress_percent': ((self.progress.total_xp % self.xp_per_level) / self.xp_per_level) * 100,
            'achievements': [asdict(ach) for ach in self.progress.achievements if ach.unlocked],
            'achievements_count': len([ach for ach in self.progress.achievements if ach.unlocked]),
            'total_achievements_count': len(self.progress.achievements)
        }
    
    def get_statistics(self, period: str = "week") -> Dict:
        """Get statistics for the specified period"""
        today = datetime.now()
        
        if period == "week":
            start_date = today - timedelta(days=today.weekday())
            days = 7
        elif period == "month":
            start_date = today.replace(day=1)
            days = 31  # Max days to check
        else:
            start_date = today - timedelta(days=7)
            days = 7
        
        daily_data = []
        total_completions = 0
        total_focus_time = 0
        
        for i in range(days):
            date = start_date + timedelta(days=i)
            if date > today:
                break
                
            date_str = date.strftime("%Y-%m-%d")
            completions = self.progress.daily_stats.get(date_str, 0)
            focus_minutes = completions * 25  # Assuming 25 min per Pomodoro
            
            daily_data.append({
                'date': date_str,
                'completions': completions,
                'focus_minutes': focus_minutes
            })
            
            total_completions += completions
            total_focus_time += focus_minutes
        
        return {
            'period': period,
            'daily_data': daily_data,
            'total_completions': total_completions,
            'total_focus_time': total_focus_time,
            'average_daily': total_completions / len(daily_data) if daily_data else 0,
            'completion_rate': min(100, (total_completions / (len(daily_data) * 8)) * 100)  # Assuming 8 Pomodoros target per day
        }