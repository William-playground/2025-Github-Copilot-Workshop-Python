/**
 * Jest setup file for DOM testing
 */

// Mock fetch for API calls
global.fetch = jest.fn();

// Set up DOM environment
beforeEach(() => {
  // Reset fetch mock
  fetch.mockClear();
  
  // Set up basic DOM structure
  document.body.innerHTML = `
    <div class="container">
      <div class="timer" id="time">25:00</div>
      <div class="buttons">
        <button id="start">開始</button>
        <button id="reset">リセット</button>
      </div>
      <div class="status">作業中</div>
      <div class="progress">
        <div class="progress-bar" style="width:40%"></div>
      </div>
      <div>
        <span id="count">0 完了</span>
        <span id="focus">0分 集中時間</span>
      </div>
    </div>
  `;
});

afterEach(() => {
  // Clean up DOM
  document.body.innerHTML = '';
  
  // Clear any timers
  jest.clearAllTimers();
});