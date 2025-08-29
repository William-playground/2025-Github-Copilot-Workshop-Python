/**
 * Pomodoro Timer with API Integration
 * Handles timer functionality and progress data sync
 */

class PomodoroTimer {
    constructor() {
        this.timeRemaining = 25 * 60; // 25 minutes in seconds
        this.isRunning = false;
        this.intervalId = null;
        this.session_time = 25; // Track session duration for API
        
        this.initializeElements();
        this.loadProgress();
        this.attachEventListeners();
    }
    
    initializeElements() {
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.countDisplay = document.getElementById('count');
        this.focusDisplay = document.getElementById('focus');
        this.progressBar = document.querySelector('.progress-bar');
    }
    
    attachEventListeners() {
        this.startButton.addEventListener('click', () => this.toggleTimer());
        this.resetButton.addEventListener('click', () => this.resetTimer());
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
        this.startButton.textContent = '一時停止';
        
        this.intervalId = setInterval(() => {
            this.timeRemaining--;
            this.updateDisplay();
            this.updateProgress();
            
            if (this.timeRemaining <= 0) {
                this.completeSession();
            }
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    resetTimer() {
        this.pauseTimer();
        this.timeRemaining = 25 * 60;
        this.updateDisplay();
        this.updateProgress();
    }
    
    async completeSession() {
        this.pauseTimer();
        
        // Send completion data to API
        try {
            await this.saveProgress(this.session_time);
            await this.loadProgress(); // Refresh progress display
        } catch (error) {
            console.error('Failed to save progress:', error);
        }
        
        // Reset timer for next session
        this.resetTimer();
        
        // Show completion message
        alert('ポモドーロセッション完了！お疲れ様でした！');
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    updateProgress() {
        const totalTime = 25 * 60;
        const elapsed = totalTime - this.timeRemaining;
        const percentage = (elapsed / totalTime) * 100;
        this.progressBar.style.width = `${percentage}%`;
    }
    
    async loadProgress() {
        try {
            const response = await fetch('/api/progress');
            if (!response.ok) {
                throw new Error('Failed to load progress');
            }
            
            const data = await response.json();
            this.updateProgressDisplay(data);
        } catch (error) {
            console.error('Failed to load progress:', error);
            // Show default values on error
            this.updateProgressDisplay({
                today: { completed_sessions: 0, focus_time: 0 }
            });
        }
    }
    
    async saveProgress(focusTime) {
        try {
            const response = await fetch('/api/progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    focus_time: focusTime
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to save progress');
            }
            
            return await response.json();
        } catch (error) {
            console.error('Failed to save progress:', error);
            throw error;
        }
    }
    
    updateProgressDisplay(data) {
        const todayData = data.today || { completed_sessions: 0, focus_time: 0 };
        
        this.countDisplay.textContent = `${todayData.completed_sessions} 完了`;
        this.focusDisplay.textContent = `${todayData.focus_time}分 集中時間`;
    }
}

// Initialize timer when page loads
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});