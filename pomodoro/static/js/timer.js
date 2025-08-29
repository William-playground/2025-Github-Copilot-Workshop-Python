let timer;
let timeLeft = 25 * 60; // 25分
let isRunning = false;

function updateDisplay() {
    const min = String(Math.floor(timeLeft / 60)).padStart(2, '0');
    const sec = String(timeLeft % 60).padStart(2, '0');
    document.getElementById('timer-display').textContent = `${min}:${sec}`;
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    timer = setInterval(() => {
        if (timeLeft > 0) {
            timeLeft--;
            updateDisplay();
        } else {
            clearInterval(timer);
            isRunning = false;
            alert('ポモドーロ終了！お疲れさまです。');
        }
    }, 1000);
}

function resetTimer() {
    clearInterval(timer);
    timeLeft = 25 * 60;
    isRunning = false;
    updateDisplay();
}

document.addEventListener('DOMContentLoaded', () => {
    updateDisplay();
    document.getElementById('start-btn').addEventListener('click', startTimer);
    document.getElementById('reset-btn').addEventListener('click', resetTimer);
});
