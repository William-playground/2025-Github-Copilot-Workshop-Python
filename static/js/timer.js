/**
 * ポモドーロタイマー フロントエンド JavaScript
 */

class PomodoroApp {
    constructor() {
        this.timerDisplay = document.getElementById('time');
        this.startButton = document.getElementById('start');
        this.resetButton = document.getElementById('reset');
        this.countDisplay = document.getElementById('count');
        this.focusDisplay = document.getElementById('focus');
        this.statusDisplay = document.querySelector('.status');
        
        this.isRunning = false;
        this.timeLeft = 25 * 60; // 25分（秒）
        this.interval = null;
        
        this.init();
    }
    
    init() {
        // イベントリスナーを設定
        this.startButton.addEventListener('click', () => this.toggleTimer());
        this.resetButton.addEventListener('click', () => this.resetTimer());
        
        // 進捗データを読み込み
        this.loadProgress();
        
        // 初期表示更新
        this.updateDisplay();
    }
    
    /**
     * 進捗データをAPIから読み込む
     */
    async loadProgress() {
        try {
            const response = await fetch('/api/progress');
            const result = await response.json();
            
            if (result.success) {
                const data = result.data;
                this.updateProgressDisplay(data.completed_sessions, data.focus_minutes);
            } else {
                console.error('進捗データの読み込みに失敗:', result.error);
            }
        } catch (error) {
            console.error('API通信エラー:', error);
        }
    }
    
    /**
     * 進捗データをAPIに保存する
     */
    async saveProgress(focusMinutes = 25) {
        try {
            const response = await fetch('/api/progress', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    focus_minutes: focusMinutes
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                const data = result.data;
                this.updateProgressDisplay(data.completed_sessions, data.focus_minutes);
                console.log('進捗データを保存しました:', data);
            } else {
                console.error('進捗データの保存に失敗:', result.error);
            }
        } catch (error) {
            console.error('API通信エラー:', error);
        }
    }
    
    /**
     * 進捗表示を更新
     */
    updateProgressDisplay(completedSessions, focusMinutes) {
        this.countDisplay.textContent = `${completedSessions} 完了`;
        this.focusDisplay.textContent = `${focusMinutes}分 集中時間`;
    }
    
    /**
     * タイマーの開始/停止を切り替え
     */
    toggleTimer() {
        if (this.isRunning) {
            this.pauseTimer();
        } else {
            this.startTimer();
        }
    }
    
    /**
     * タイマーを開始
     */
    startTimer() {
        this.isRunning = true;
        this.startButton.textContent = '停止';
        this.statusDisplay.textContent = '作業中';
        
        this.interval = setInterval(() => {
            this.timeLeft--;
            this.updateDisplay();
            
            if (this.timeLeft <= 0) {
                this.completeSession();
            }
        }, 1000);
    }
    
    /**
     * タイマーを一時停止
     */
    pauseTimer() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        clearInterval(this.interval);
    }
    
    /**
     * タイマーをリセット
     */
    resetTimer() {
        this.isRunning = false;
        this.timeLeft = 25 * 60;
        this.startButton.textContent = '開始';
        this.statusDisplay.textContent = '作業中';
        clearInterval(this.interval);
        this.updateDisplay();
    }
    
    /**
     * セッション完了時の処理
     */
    completeSession() {
        this.isRunning = false;
        this.startButton.textContent = '開始';
        this.statusDisplay.textContent = 'セッション完了！';
        clearInterval(this.interval);
        
        // 進捗データを保存
        this.saveProgress(25);
        
        // 5秒後にリセット
        setTimeout(() => {
            this.resetTimer();
        }, 5000);
    }
    
    /**
     * 表示を更新
     */
    updateDisplay() {
        const minutes = Math.floor(this.timeLeft / 60);
        const seconds = this.timeLeft % 60;
        this.timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
}

// DOMが読み込まれたらアプリを初期化
document.addEventListener('DOMContentLoaded', () => {
    new PomodoroApp();
});