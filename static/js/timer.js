/**
 * Pomodoro Timer with Gamification
 * Handles timer functionality and integrates with gamification system
 */

class PomodoroTimer {
    constructor() {
        this.workMinutes = 25;
        this.breakMinutes = 5;
        this.isRunning = false;
        this.isWorkSession = true;
        this.timeLeft = this.workMinutes * 60;
        this.totalTime = this.workMinutes * 60;
        
        this.initializeElements();
        this.loadProgress();
        this.updateDisplay();
        this.setupEventListeners();
    }
    
    initializeElements() {
        // Timer elements
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.statusDisplay = document.getElementById('status');
        this.timerProgress = document.getElementById('timer-progress');
        
        // Stats elements
        this.countDisplay = document.getElementById('count');
        this.focusDisplay = document.getElementById('focus');
        
        // Gamification elements
        this.levelDisplay = document.getElementById('player-level');
        this.currentXpDisplay = document.getElementById('current-xp');
        this.xpToNextDisplay = document.getElementById('xp-to-next');
        this.xpProgress = document.getElementById('xp-progress');
        this.currentStreakDisplay = document.getElementById('current-streak');
        this.achievementsCountDisplay = document.getElementById('achievements-count');
        this.totalAchievementsDisplay = document.getElementById('total-achievements');
        
        // Notification elements
        this.achievementNotification = document.getElementById('achievement-notification');
        this.levelUpNotification = document.getElementById('level-up-notification');
        
        // Sections
        this.achievementsSection = document.getElementById('achievements-section');
        this.statisticsSection = document.getElementById('statistics-section');
        this.achievementsGrid = document.getElementById('achievements-grid');
    }
    
    setupEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleTimer());
        this.resetButton.addEventListener('click', () => this.resetTimer());
    }
    
    async loadProgress() {
        try {
            const response = await fetch('/api/progress');
            const progress = await response.json();
            this.updateGamificationDisplay(progress);
            
            // Load achievements
            await this.loadAchievements();
            
        } catch (error) {
            console.error('Failed to load progress:', error);
        }
    }
    
    async loadAchievements() {
        try {
            const response = await fetch('/api/achievements');
            const achievements = await response.json();
            this.renderAchievements(achievements);
            
            // Update counts
            const unlockedCount = achievements.filter(a => a.unlocked).length;
            this.achievementsCountDisplay.textContent = unlockedCount;
            this.totalAchievementsDisplay.textContent = achievements.length;
            
            // Show achievements section if there are any unlocked
            if (unlockedCount > 0) {
                this.achievementsSection.style.display = 'block';
            }
            
        } catch (error) {
            console.error('Failed to load achievements:', error);
        }
    }
    
    renderAchievements(achievements) {
        this.achievementsGrid.innerHTML = '';
        
        achievements.forEach(achievement => {
            const achievementElement = document.createElement('div');
            achievementElement.className = `achievement-item ${achievement.unlocked ? 'unlocked' : ''}`;
            
            if (!achievement.unlocked) {
                achievementElement.style.opacity = '0.5';
            }
            
            achievementElement.innerHTML = `
                <div class="achievement-icon">${achievement.icon}</div>
                <div class="achievement-name">${achievement.name}</div>
                <div class="achievement-description">${achievement.description}</div>
            `;
            
            this.achievementsGrid.appendChild(achievementElement);
        });
    }
    
    updateGamificationDisplay(progress) {
        this.levelDisplay.textContent = progress.level;
        this.currentXpDisplay.textContent = progress.total_xp;
        this.xpToNextDisplay.textContent = progress.xp_to_next_level;
        this.currentStreakDisplay.textContent = progress.current_streak;
        this.countDisplay.textContent = `${progress.completed_pomodoros} 完了`;
        this.focusDisplay.textContent = `${progress.focus_time_minutes}分 集中時間`;
        
        // Update XP progress bar
        this.xpProgress.style.width = `${progress.xp_progress_percent}%`;
    }
    
    toggleTimer() {
        if (this.isRunning) {
            this.pauseTimer();
        } else {
            this.startTimer();
        }
    }
    
    startTimer() {
        this.isRunning = true;
        this.startButton.textContent = 'ポーズ';
        this.startButton.style.background = '#f39c12';
        
        this.timer = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.completeSession();
            }
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        this.startButton.style.background = '#e74c3c';
        clearInterval(this.timer);
    }
    
    resetTimer() {
        this.pauseTimer();
        this.timeLeft = this.isWorkSession ? this.workMinutes * 60 : this.breakMinutes * 60;
        this.totalTime = this.timeLeft;
        this.updateDisplay();
    }
    
    async completeSession() {
        this.pauseTimer();
        
        if (this.isWorkSession) {
            // Work session completed - award XP
            await this.awardXP();
            
            // Switch to break
            this.isWorkSession = false;
            this.timeLeft = this.breakMinutes * 60;
            this.statusDisplay.textContent = '休憩中';
        } else {
            // Break completed - switch back to work
            this.isWorkSession = true;
            this.timeLeft = this.workMinutes * 60;
            this.statusDisplay.textContent = '作業中';
        }
        
        this.totalTime = this.timeLeft;
        this.updateDisplay();
        
        // Play notification sound (if supported)
        this.playNotificationSound();
    }
    
    async awardXP() {
        try {
            const response = await fetch('/api/progress/complete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    focus_minutes: this.workMinutes
                })
            });
            
            const result = await response.json();
            
            // Update display
            this.updateGamificationDisplay(result);
            
            // Show level up notification
            if (result.level_up) {
                this.showLevelUpNotification(result.level);
            }
            
            // Show achievement notifications
            if (result.new_achievements && result.new_achievements.length > 0) {
                for (const achievement of result.new_achievements) {
                    this.showAchievementNotification(achievement);
                }
                
                // Reload achievements to update display
                await this.loadAchievements();
            }
            
        } catch (error) {
            console.error('Failed to award XP:', error);
        }
    }
    
    showLevelUpNotification(newLevel) {
        const notification = this.levelUpNotification;
        const text = document.getElementById('level-up-text');
        text.textContent = `レベル ${newLevel} に到達しました！`;
        
        notification.classList.add('show');
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 4000);
    }
    
    showAchievementNotification(achievement) {
        const notification = this.achievementNotification;
        const icon = document.getElementById('notification-icon');
        const title = document.getElementById('notification-title');
        const description = document.getElementById('notification-description');
        
        icon.textContent = achievement.icon;
        title.textContent = achievement.name;
        description.textContent = achievement.description;
        
        notification.classList.add('show');
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 5000);
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        this.timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update progress bar
        const progress = ((this.totalTime - this.timeLeft) / this.totalTime) * 100;
        this.timerProgress.style.width = `${progress}%`;
        
        // Update status
        this.statusDisplay.textContent = this.isWorkSession ? '作業中' : '休憩中';
    }
    
    playNotificationSound() {
        // Simple audio notification using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = 800;
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            console.log('Audio notification not supported');
        }
    }
}

// Statistics and UI functions
async function loadStatistics(period = 'week') {
    try {
        const response = await fetch(`/api/statistics?period=${period}`);
        const stats = await response.json();
        
        renderStatistics(stats);
        
        // Update active button - fix the event reference
        document.querySelectorAll('.stats-period-selector button').forEach(btn => {
            btn.classList.remove('active');
        });
        
        // Find and activate the correct button
        const buttons = document.querySelectorAll('.stats-period-selector button');
        buttons.forEach(btn => {
            if ((period === 'week' && btn.textContent === '週間') ||
                (period === 'month' && btn.textContent === '月間')) {
                btn.classList.add('active');
            }
        });
        
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

function renderStatistics(stats) {
    const summaryElement = document.getElementById('stats-summary');
    const chartElement = document.getElementById('stats-chart');
    
    // Render summary
    summaryElement.innerHTML = `
        <div class="stat-item">
            <div class="stat-value">${stats.total_completions}</div>
            <div class="stat-label">完了回数</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${Math.round(stats.total_focus_time / 60)}h</div>
            <div class="stat-label">集中時間</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${stats.average_daily.toFixed(1)}</div>
            <div class="stat-label">平均/日</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">${Math.round(stats.completion_rate)}%</div>
            <div class="stat-label">達成率</div>
        </div>
    `;
    
    // Render chart
    const maxCompletions = Math.max(...stats.daily_data.map(d => d.completions), 1);
    chartElement.innerHTML = stats.daily_data.map(day => {
        const date = new Date(day.date);
        const dayLabel = ['日', '月', '火', '水', '木', '金', '土'][date.getDay()];
        const barWidth = (day.completions / maxCompletions) * 100;
        
        return `
            <div class="chart-day">
                <div class="chart-day-label">${dayLabel}</div>
                <div class="chart-bar-container">
                    <div class="chart-bar" style="width: ${barWidth}%"></div>
                </div>
                <div class="chart-value">${day.completions}</div>
            </div>
        `;
    }).join('');
}

function toggleStatsView() {
    const statsSection = document.getElementById('statistics-section');
    const button = document.getElementById('toggle-stats');
    
    if (statsSection.style.display === 'none') {
        statsSection.style.display = 'block';
        button.textContent = '📊 統計を非表示';
        loadStatistics('week');
    } else {
        statsSection.style.display = 'none';
        button.textContent = '📊 統計を表示';
    }
}

// Initialize the timer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});