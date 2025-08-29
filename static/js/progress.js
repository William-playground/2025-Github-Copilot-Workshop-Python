/**
 * 進捗管理のフロントエンド表示
 * Stage 4: Frontend Progress Display with dummy data
 */

// ダミーデータ：今日の進捗情報
const progressData = {
    completedPomodoros: 3,      // 今日完了したポモドーロ数
    totalFocusTime: 75,         // 累計集中時間（分）
    currentDate: new Date().toLocaleDateString('ja-JP')
};

/**
 * 進捗表示を更新する関数
 */
function updateProgressDisplay() {
    const countElement = document.getElementById('count');
    const focusElement = document.getElementById('focus');
    
    if (countElement) {
        countElement.textContent = `${progressData.completedPomodoros} 完了`;
    }
    
    if (focusElement) {
        focusElement.textContent = `${progressData.totalFocusTime}分 集中時間`;
    }
}

/**
 * プログレスバーを更新する関数
 * （仮の実装：完了したポモドーロ数に基づいて進捗率を計算）
 */
function updateProgressBar() {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        // 1日の目標を8ポモドーロと仮定して進捗率を計算
        const dailyGoal = 8;
        const progressPercentage = Math.min((progressData.completedPomodoros / dailyGoal) * 100, 100);
        progressBar.style.width = `${progressPercentage}%`;
    }
}

/**
 * 進捗データをローカルストレージから読み込む（将来の拡張用）
 */
function loadProgressData() {
    // 現在はダミーデータを使用
    // 将来的にはAPIから取得またはローカルストレージから読み込み
    console.log('Current progress data:', progressData);
}

/**
 * DOM読み込み完了時に実行
 */
document.addEventListener('DOMContentLoaded', function() {
    console.log('Progress display initialized');
    loadProgressData();
    updateProgressDisplay();
    updateProgressBar();
});

/**
 * 進捗データを更新する公開関数（将来のタイマー機能との連携用）
 */
function incrementCompletedPomodoros() {
    progressData.completedPomodoros++;
    progressData.totalFocusTime += 25; // 1ポモドーロ = 25分
    updateProgressDisplay();
    updateProgressBar();
}

// 公開関数をwindowオブジェクトに追加（他のスクリプトからアクセス可能にする）
window.progressManager = {
    updateProgressDisplay,
    updateProgressBar,
    incrementCompletedPomodoros,
    progressData
};