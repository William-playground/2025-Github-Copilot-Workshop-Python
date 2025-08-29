/**
 * Tests for PomodoroTimer JavaScript class
 */

// Import the timer class
const PomodoroTimer = require('../static/js/timer.js');

// Mock timers
jest.useFakeTimers();

describe('PomodoroTimer', () => {
  let timer;

  beforeEach(() => {
    timer = new PomodoroTimer();
  });

  afterEach(() => {
    if (timer.intervalId) {
      clearInterval(timer.intervalId);
    }
  });

  describe('Initialization', () => {
    test('should initialize with correct default values', () => {
      expect(timer.getTimeRemaining()).toBe(25 * 60); // 25 minutes
      expect(timer.getIsRunning()).toBe(false);
      expect(timer.getIsWorkSession()).toBe(true);
      expect(timer.workDuration).toBe(25 * 60);
      expect(timer.breakDuration).toBe(5 * 60);
    });

    test('should update display on initialization', () => {
      const timeElement = document.getElementById('time');
      expect(timeElement.textContent).toBe('25:00');
    });
  });

  describe('Timer Controls', () => {
    test('should start timer when not running', () => {
      timer.startTimer();
      expect(timer.getIsRunning()).toBe(true);
      expect(timer.intervalId).toBeTruthy();
    });

    test('should pause timer when running', () => {
      timer.startTimer();
      timer.pauseTimer();
      expect(timer.getIsRunning()).toBe(false);
      expect(timer.intervalId).toBe(null);
    });

    test('should toggle timer state', () => {
      // Initially stopped
      expect(timer.getIsRunning()).toBe(false);
      
      // Toggle to start
      timer.toggleTimer();
      expect(timer.getIsRunning()).toBe(true);
      
      // Toggle to pause
      timer.toggleTimer();
      expect(timer.getIsRunning()).toBe(false);
    });

    test('should reset timer to work duration', () => {
      timer.setTimeRemaining(300); // 5 minutes
      timer.resetTimer();
      expect(timer.getTimeRemaining()).toBe(25 * 60);
      expect(timer.getIsRunning()).toBe(false);
    });
  });

  describe('Timer Countdown', () => {
    test('should countdown when running', () => {
      timer.startTimer();
      
      // Fast-forward time
      jest.advanceTimersByTime(3000); // 3 seconds
      
      expect(timer.getTimeRemaining()).toBe(25 * 60 - 3);
    });

    test('should update display during countdown', () => {
      timer.setTimeRemaining(65); // 1:05
      timer.updateDisplay();
      
      const timeElement = document.getElementById('time');
      expect(timeElement.textContent).toBe('01:05');
    });

    test('should format time correctly', () => {
      timer.setTimeRemaining(3661); // 61:01
      timer.updateDisplay();
      
      const timeElement = document.getElementById('time');
      expect(timeElement.textContent).toBe('61:01');
    });
  });

  describe('Progress Bar', () => {
    test('should update progress bar based on time remaining', () => {
      timer.setTimeRemaining(15 * 60); // Half way through work session
      timer.updateProgressBar();
      
      const progressBar = document.querySelector('.progress-bar');
      expect(progressBar.style.width).toBe('40%'); // (25-15)/25 * 100
    });

    test('should show 100% progress when time is up', () => {
      timer.setTimeRemaining(0);
      timer.updateProgressBar();
      
      const progressBar = document.querySelector('.progress-bar');
      expect(progressBar.style.width).toBe('100%');
    });
  });

  describe('Work/Break Sessions', () => {
    test('should switch to break after work completion', () => {
      // Mock the API call
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: {} })
      });

      timer.switchToBreak();
      
      expect(timer.getIsWorkSession()).toBe(false);
      expect(timer.getTimeRemaining()).toBe(5 * 60);
    });

    test('should switch to work after break completion', () => {
      timer.switchToWork();
      
      expect(timer.getIsWorkSession()).toBe(true);
      expect(timer.getTimeRemaining()).toBe(25 * 60);
    });

    test('should update status when switching sessions', () => {
      timer.switchToBreak();
      const statusElement = document.querySelector('.status');
      expect(statusElement.textContent).toBe('休憩中');

      timer.switchToWork();
      expect(statusElement.textContent).toBe('作業中');
    });
  });

  describe('Session Completion', () => {
    test('should complete work session and switch to break', () => {
      // Mock the API call
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: {} })
      });

      timer.completeSession();
      
      expect(timer.getIsRunning()).toBe(false);
      expect(timer.getIsWorkSession()).toBe(false);
      expect(timer.getTimeRemaining()).toBe(5 * 60);
    });

    test('should complete break session and switch to work', () => {
      timer.switchToBreak();
      timer.completeSession();
      
      expect(timer.getIsRunning()).toBe(false);
      expect(timer.getIsWorkSession()).toBe(true);
      expect(timer.getTimeRemaining()).toBe(25 * 60);
    });

    test('should call API when work session completes', async () => {
      // Mock successful API response
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: { today_completed: 1, today_focus_time: 25 } })
      });

      await timer.addCompletedSession();

      expect(fetch).toHaveBeenCalledWith('/api/progress', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'complete_session',
          focus_time: 25
        })
      });
    });
  });

  describe('API Communication', () => {
    test('should load progress data on initialization', async () => {
      const mockData = {
        success: true,
        data: {
          today_completed: 3,
          today_focus_time: 75
        }
      };

      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve(mockData)
      });

      await timer.loadProgress();

      expect(fetch).toHaveBeenCalledWith('/api/progress');
    });

    test('should update progress display with API data', () => {
      const progressData = {
        today_completed: 5,
        today_focus_time: 125
      };

      timer.updateProgressDisplay(progressData);

      const countElement = document.getElementById('count');
      const focusElement = document.getElementById('focus');

      expect(countElement.textContent).toBe('5 完了');
      expect(focusElement.textContent).toBe('125分 集中時間');
    });

    test('should handle API errors gracefully', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));
      
      // Should not throw
      await expect(timer.loadProgress()).resolves.toBeUndefined();
    });
  });

  describe('Button Updates', () => {
    test('should update start button text when running', () => {
      timer.startTimer();
      const startBtn = document.getElementById('start');
      expect(startBtn.textContent).toBe('一時停止');
    });

    test('should update start button text when paused', () => {
      timer.startTimer();
      timer.pauseTimer();
      const startBtn = document.getElementById('start');
      expect(startBtn.textContent).toBe('開始');
    });
  });

  describe('Timer Completion Flow', () => {
    test('should handle complete timer countdown', () => {
      // Mock API for session completion
      global.fetch.mockResolvedValueOnce({
        json: () => Promise.resolve({ success: true, data: {} })
      });

      timer.setTimeRemaining(2); // 2 seconds left
      timer.startTimer();

      // Fast-forward past completion
      jest.advanceTimersByTime(3000);

      expect(timer.getIsRunning()).toBe(false);
      expect(timer.getIsWorkSession()).toBe(false); // Should switch to break
    });
  });
});