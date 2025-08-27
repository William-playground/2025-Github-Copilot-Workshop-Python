// ポモドーロタイマー JavaScript

class PomodoroTimer {
    constructor() {
        this.settings = this.loadSettings();
        this.timeRemaining = this.settings.workDuration * 60; // 秒に変換
        this.isRunning = false;
        this.isBreak = false;
        this.timer = null;
        this.completedSessions = 0;
        this.totalFocusTime = 0;
        
        this.initializeElements();
        this.updateDisplay();
        this.applyTheme();
        this.bindEvents();
    }

    loadSettings() {
        const defaultSettings = {
            workDuration: 25, // 分
            breakDuration: 5, // 分
            theme: 'light',
            sounds: {
                start: true,
                end: true,
                tick: false
            }
        };
        
        const saved = localStorage.getItem('pomodoroSettings');
        return saved ? { ...defaultSettings, ...JSON.parse(saved) } : defaultSettings;
    }

    saveSettings() {
        localStorage.setItem('pomodoroSettings', JSON.stringify(this.settings));
    }

    initializeElements() {
        this.timeElement = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.statusElement = document.querySelector('.status');
        this.progressBar = document.querySelector('.progress-bar');
        this.countElement = document.getElementById('count');
        this.focusElement = document.getElementById('focus');
    }

    bindEvents() {
        this.startButton.addEventListener('click', () => this.toggleTimer());
        this.resetButton.addEventListener('click', () => this.resetTimer());
        
        // 設定ボタンイベント（後で追加）
        const settingsBtn = document.getElementById('settings-btn');
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => this.openSettings());
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
        this.startButton.textContent = '停止';
        
        if (this.settings.sounds.start) {
            this.playSound('start');
        }
        
        this.timer = setInterval(() => {
            this.timeRemaining--;
            this.updateDisplay();
            
            if (this.settings.sounds.tick) {
                this.playSound('tick');
            }
            
            if (this.timeRemaining <= 0) {
                this.completeSession();
            }
        }, 1000);
    }

    pauseTimer() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        clearInterval(this.timer);
    }

    resetTimer() {
        this.pauseTimer();
        this.timeRemaining = this.isBreak ? 
            this.settings.breakDuration * 60 : 
            this.settings.workDuration * 60;
        this.updateDisplay();
    }

    completeSession() {
        this.pauseTimer();
        
        if (this.settings.sounds.end) {
            this.playSound('end');
        }
        
        if (!this.isBreak) {
            this.completedSessions++;
            this.totalFocusTime += this.settings.workDuration;
            this.isBreak = true;
            this.timeRemaining = this.settings.breakDuration * 60;
            this.statusElement.textContent = '休憩中';
        } else {
            this.isBreak = false;
            this.timeRemaining = this.settings.workDuration * 60;
            this.statusElement.textContent = '作業中';
        }
        
        this.updateDisplay();
        this.updateStats();
    }

    updateDisplay() {
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timeElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // プログレスバー更新
        const totalTime = this.isBreak ? this.settings.breakDuration * 60 : this.settings.workDuration * 60;
        const progress = ((totalTime - this.timeRemaining) / totalTime) * 100;
        this.progressBar.style.width = `${progress}%`;
    }

    updateStats() {
        this.countElement.textContent = `${this.completedSessions} 完了`;
        this.focusElement.textContent = `${this.totalFocusTime}分 集中時間`;
    }

    playSound(type) {
        // 簡単な音の実装（実際の音ファイルは省略）
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance();
            switch(type) {
                case 'start':
                    utterance.text = 'スタート';
                    break;
                case 'end':
                    utterance.text = '終了';
                    break;
                case 'tick':
                    // tick音は省略（頻繁すぎるため）
                    return;
            }
            utterance.volume = 0.1;
            utterance.rate = 1.5;
            speechSynthesis.speak(utterance);
        }
    }

    applyTheme() {
        document.body.className = `theme-${this.settings.theme}`;
    }

    openSettings() {
        // 設定モーダルを開く（後で実装）
        console.log('設定を開く');
    }

    updateSettings(newSettings) {
        this.settings = { ...this.settings, ...newSettings };
        this.saveSettings();
        this.applyTheme();
        this.resetTimer();
    }
}

// ページ読み込み時に初期化
document.addEventListener('DOMContentLoaded', () => {
    window.pomodoroTimer = new PomodoroTimer();
});