// ポモドーロタイマー JavaScript
class PomodoroTimer {
    constructor() {
        // Timer state
        this.isRunning = false;
        this.isPaused = false;
        this.totalSeconds = 25 * 60; // 25 minutes default
        this.currentSeconds = this.totalSeconds;
        this.intervalId = null;
        this.isWorkSession = true; // true = work, false = break
        
        // DOM elements
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.statusDisplay = document.querySelector('.status');
        this.progressBar = document.querySelector('.progress-bar');
        
        // Initialize
        this.initializeEventListeners();
        this.updateDisplay();
    }
    
    initializeEventListeners() {
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
        this.isPaused = false;
        this.startButton.textContent = '一時停止';
        
        this.intervalId = setInterval(() => {
            this.currentSeconds--;
            this.updateDisplay();
            
            if (this.currentSeconds <= 0) {
                this.timerComplete();
            }
        }, 1000);
    }
    
    pauseTimer() {
        this.isRunning = false;
        this.isPaused = true;
        this.startButton.textContent = '再開';
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    resetTimer() {
        this.isRunning = false;
        this.isPaused = false;
        this.currentSeconds = this.totalSeconds;
        this.startButton.textContent = '開始';
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        this.updateDisplay();
    }
    
    timerComplete() {
        this.isRunning = false;
        this.isPaused = false;
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        
        // Show notification
        this.showNotification();
        
        // Play notification sound
        this.playNotificationSound();
        
        // Switch between work and break
        this.switchSession();
    }
    
    showNotification() {
        const message = this.isWorkSession 
            ? 'ポモドーロ完了！お疲れ様でした。休憩時間です。'
            : '休憩時間終了！作業を再開しましょう。';
        
        // Browser notification (if permission granted)
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('ポモドーロタイマー', {
                body: message,
                icon: '/static/favicon.ico' // if you have a favicon
            });
        } else {
            // Fallback to alert
            alert(message);
        }
    }
    
    playNotificationSound() {
        // Create audio context for notification sound
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.setValueAtTime(600, audioContext.currentTime + 0.1);
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 0.2);
            
            gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.5);
        } catch (error) {
            console.log('Audio notification not supported:', error);
        }
    }
    
    switchSession() {
        this.isWorkSession = !this.isWorkSession;
        
        if (this.isWorkSession) {
            this.totalSeconds = 25 * 60; // 25 minutes work
            this.statusDisplay.textContent = '作業中';
        } else {
            this.totalSeconds = 5 * 60; // 5 minutes break
            this.statusDisplay.textContent = '休憩中';
        }
        
        this.currentSeconds = this.totalSeconds;
        this.startButton.textContent = '開始';
        this.updateDisplay();
    }
    
    updateDisplay() {
        // Update time display
        const minutes = Math.floor(this.currentSeconds / 60);
        const seconds = this.currentSeconds % 60;
        this.timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update progress bar
        const progress = ((this.totalSeconds - this.currentSeconds) / this.totalSeconds) * 100;
        this.progressBar.style.width = `${progress}%`;
    }
    
    // Request notification permission on initialization
    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
}

// Initialize timer when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    const timer = new PomodoroTimer();
    timer.requestNotificationPermission();
});