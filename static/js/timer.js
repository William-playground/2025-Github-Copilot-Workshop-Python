/**
 * Pomodoro Timer Logic
 * Handles timer functionality, progress tracking, and UI updates
 */

class PomodoroTimer {
    constructor() {
        this.timeLeft = 25 * 60; // 25 minutes in seconds
        this.defaultTime = 25 * 60;
        this.isRunning = false;
        this.timer = null;
        
        // UI elements
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.statusDisplay = document.querySelector('.status');
        this.progressBar = document.querySelector('.progress-bar');
        this.countDisplay = document.getElementById('count');
        this.focusDisplay = document.getElementById('focus');
        
        this.initializeEventListeners();
        this.loadProgress();
    }
    
    initializeEventListeners() {
        if (this.startButton) {
            this.startButton.addEventListener('click', () => this.toggleTimer());
        }
        if (this.resetButton) {
            this.resetButton.addEventListener('click', () => this.resetTimer());
        }
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    updateDisplay() {
        if (this.timeDisplay) {
            this.timeDisplay.textContent = this.formatTime(this.timeLeft);
        }
        
        // Update progress bar
        const progress = ((this.defaultTime - this.timeLeft) / this.defaultTime) * 100;
        if (this.progressBar) {
            this.progressBar.style.width = `${progress}%`;
        }
        
        // Update status
        if (this.statusDisplay) {
            this.statusDisplay.textContent = this.isRunning ? '作業中' : '一時停止';
        }
    }
    
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        if (this.startButton) {
            this.startButton.textContent = '停止';
        }
        
        this.timer = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.completeSession();
            }
        }, 1000);
        
        this.updateDisplay();
    }
    
    stop() {
        if (!this.isRunning) return;
        
        this.isRunning = false;
        if (this.startButton) {
            this.startButton.textContent = '開始';
        }
        
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
        
        this.updateDisplay();
    }
    
    toggleTimer() {
        if (this.isRunning) {
            this.stop();
        } else {
            this.start();
        }
    }
    
    resetTimer() {
        this.stop();
        this.timeLeft = this.defaultTime;
        this.updateDisplay();
    }
    
    async completeSession() {
        this.stop();
        this.timeLeft = this.defaultTime;
        
        // Send completed session to backend
        try {
            await this.saveProgress();
            await this.loadProgress();
        } catch (error) {
            console.error('Error saving progress:', error);
        }
        
        this.updateDisplay();
        alert('ポモドーロセッション完了！お疲れさまでした。');
    }
    
    async saveProgress() {
        try {
            const response = await fetch('/api/progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    session_duration: 25
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Failed to save progress:', error);
            throw error;
        }
    }
    
    async loadProgress() {
        try {
            const response = await fetch('/api/progress');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.updateProgressDisplay(data);
        } catch (error) {
            console.error('Failed to load progress:', error);
            // Continue with default values if API is not available
            this.updateProgressDisplay({
                completed_sessions: 0,
                focus_time: 0
            });
        }
    }
    
    updateProgressDisplay(data) {
        if (this.countDisplay) {
            this.countDisplay.textContent = `${data.completed_sessions || 0} 完了`;
        }
        if (this.focusDisplay) {
            this.focusDisplay.textContent = `${data.focus_time || 0}分 集中時間`;
        }
    }
}

// Timer utility functions for testing
const TimerUtils = {
    formatTime: (seconds) => {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    },
    
    calculateProgress: (timeLeft, totalTime) => {
        return ((totalTime - timeLeft) / totalTime) * 100;
    },
    
    validateTimeInput: (timeInMinutes) => {
        return timeInMinutes > 0 && timeInMinutes <= 120; // Max 2 hours
    }
};

// Initialize timer when DOM is loaded
if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
        window.pomodoroTimer = new PomodoroTimer();
    });
}

// Export for testing (Node.js environment)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { PomodoroTimer, TimerUtils };
}