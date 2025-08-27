// ポモドーロタイマー JavaScript
class PomodoroTimer {
    constructor() {
        // タイマー設定（秒単位）
        this.WORK_TIME = 25 * 60; // 25分
        this.BREAK_TIME = 5 * 60; // 5分
        
        // 現在の状態
        this.timeRemaining = this.WORK_TIME;
        this.isRunning = false;
        this.isWorkPhase = true; // true: 作業中, false: 休憩中
        this.intervalId = null;
        
        // DOM要素の取得
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.statusDisplay = document.querySelector('.status');
        this.progressBar = document.querySelector('.progress-bar');
        
        // イベントリスナーの設定
        this.setupEventListeners();
        
        // 初期表示の更新
        this.updateDisplay();
    }
    
    setupEventListeners() {
        this.startButton.addEventListener('click', () => {
            this.toggleTimer();
        });
        
        this.resetButton.addEventListener('click', () => {
            this.resetTimer();
        });
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
            
            if (this.timeRemaining <= 0) {
                this.switchPhase();
            }
            
            this.updateDisplay();
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
        this.isWorkPhase = true;
        this.timeRemaining = this.WORK_TIME;
        this.updateDisplay();
    }
    
    switchPhase() {
        this.isWorkPhase = !this.isWorkPhase;
        this.timeRemaining = this.isWorkPhase ? this.WORK_TIME : this.BREAK_TIME;
        
        // 作業完了時の処理（今後の実装で使用）
        if (this.isWorkPhase) {
            // 休憩が終わって作業に戻る時
            console.log('Break completed, starting work session');
        } else {
            // 作業が終わって休憩に入る時
            console.log('Work session completed, starting break');
        }
    }
    
    updateDisplay() {
        // 時間表示の更新
        const minutes = Math.floor(this.timeRemaining / 60);
        const seconds = this.timeRemaining % 60;
        this.timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // ステータス表示の更新
        this.statusDisplay.textContent = this.isWorkPhase ? '作業中' : '休憩中';
        
        // プログレスバーの更新
        const totalTime = this.isWorkPhase ? this.WORK_TIME : this.BREAK_TIME;
        const progress = ((totalTime - this.timeRemaining) / totalTime) * 100;
        this.progressBar.style.width = `${progress}%`;
    }
    
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
}

// ページ読み込み完了後にタイマーを初期化
document.addEventListener('DOMContentLoaded', () => {
    window.pomodoroTimer = new PomodoroTimer();
});