/**
 * Pomodoro Timer JavaScript Logic
 * Handles timer functionality and API communication
 */

class PomodoroTimer {
    constructor() {
        this.timeRemaining = 25 * 60; // 25 minutes in seconds
        this.isRunning = false;
        this.isWorkSession = true;
        this.intervalId = null;
        this.workDuration = 25 * 60; // 25 minutes
        this.breakDuration = 5 * 60; // 5 minutes
        
        this.bindEvents();
        this.updateDisplay();
        this.loadProgress();
    }
    
    bindEvents() {
        const startBtn = document.getElementById('start');
        const resetBtn = document.getElementById('reset');
        
        if (startBtn) {
            startBtn.addEventListener('click', () => this.toggleTimer());
        }
        
        if (resetBtn) {
            resetBtn.addEventListener('click', () => this.resetTimer());
        }
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
        this.updateStartButton();
        
        this.intervalId = setInterval(() => {
            this.timeRemaining--;
            this.updateDisplay();
            this.updateProgressBar();
            
            if (this.timeRemaining <= 0) {
                this.completeSession();
            }
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.updateStartButton();
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    resetTimer() {
        this.pauseTimer();
        this.timeRemaining = this.isWorkSession ? this.workDuration : this.breakDuration;
        this.updateDisplay();
        this.updateProgressBar();
    }
    
    completeSession() {
        this.pauseTimer();
        
        if (this.isWorkSession) {
            // Work session completed - add to progress
            this.addCompletedSession();
            this.switchToBreak();
        } else {
            // Break completed - switch back to work
            this.switchToWork();
        }
    }
    
    switchToWork() {
        this.isWorkSession = true;
        this.timeRemaining = this.workDuration;
        this.updateDisplay();
        this.updateStatus();
        this.updateProgressBar();
    }
    
    switchToBreak() {
        this.isWorkSession = false;
        this.timeRemaining = this.breakDuration;
        this.updateDisplay();
        this.updateStatus();
        this.updateProgressBar();
    }
    
    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        const timeElement = document.getElementById('time');
        if (timeElement) {
            timeElement.textContent = timeString;
        }
    }
    
    updateStartButton() {
        const startBtn = document.getElementById('start');
        if (startBtn) {
            startBtn.textContent = this.isRunning ? '一時停止' : '開始';
        }
    }
    
    updateStatus() {
        const statusElement = document.querySelector('.status');
        if (statusElement) {
            statusElement.textContent = this.isWorkSession ? '作業中' : '休憩中';
        }
    }
    
    updateProgressBar() {
        const totalTime = this.isWorkSession ? this.workDuration : this.breakDuration;
        const progress = ((totalTime - this.timeRemaining) / totalTime) * 100;
        
        const progressBar = document.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
    }
    
    async loadProgress() {
        try {
            const response = await fetch('/api/progress');
            const result = await response.json();
            
            if (result.success) {
                this.updateProgressDisplay(result.data);
            }
        } catch (error) {
            console.error('Failed to load progress:', error);
        }
    }
    
    async addCompletedSession() {
        try {
            const response = await fetch('/api/progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    action: 'complete_session',
                    focus_time: 25
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.updateProgressDisplay(result.data);
            }
        } catch (error) {
            console.error('Failed to update progress:', error);
        }
    }
    
    updateProgressDisplay(progressData) {
        const countElement = document.getElementById('count');
        const focusElement = document.getElementById('focus');
        
        if (countElement) {
            countElement.textContent = `${progressData.today_completed} 完了`;
        }
        
        if (focusElement) {
            focusElement.textContent = `${progressData.today_focus_time}分 集中時間`;
        }
    }
    
    // Utility methods for testing
    getTimeRemaining() {
        return this.timeRemaining;
    }
    
    getIsRunning() {
        return this.isRunning;
    }
    
    getIsWorkSession() {
        return this.isWorkSession;
    }
    
    setTimeRemaining(seconds) {
        this.timeRemaining = seconds;
        this.updateDisplay();
    }
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.pomodoroTimer = new PomodoroTimer();
});

// Export for testing (if in Node.js environment)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PomodoroTimer;
}