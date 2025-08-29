// ポモドーロタイマー JavaScript
class PomodoroTimer {
    constructor() {
        this.timeLeft = 25 * 60; // 25分（秒単位）
        this.isRunning = false;
        this.intervalId = null;
        
        // DOM要素の取得
        this.timeDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        
        // イベントリスナーの設定
        this.startButton.addEventListener('click', () => this.toggleTimer());
        this.resetButton.addEventListener('click', () => this.resetTimer());
        
        // 初期表示の更新
        this.updateDisplay();
    }
    
    // タイマーの開始/停止を切り替える
    toggleTimer() {
        if (this.isRunning) {
            this.stopTimer();
        } else {
            this.startTimer();
        }
    }
    
    // タイマーを開始する
    startTimer() {
        this.isRunning = true;
        this.startButton.textContent = '停止';
        
        this.intervalId = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.stopTimer();
                this.onTimerComplete();
            }
        }, 1000);
    }
    
    // タイマーを停止する
    stopTimer() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    // タイマーをリセットする
    resetTimer() {
        this.stopTimer();
        this.timeLeft = 25 * 60; // 25分にリセット
        this.updateDisplay();
    }
    
    // 表示を更新する
    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        const timeString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        this.timeDisplay.textContent = timeString;
    }
    
    // タイマー完了時の処理
    onTimerComplete() {
        alert('ポモドーロタイマーが完了しました！');
        this.resetTimer();
    }
}

// ページ読み込み完了後にタイマーを初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});