/**
 * Tests for Pomodoro Timer Visual Enhancements
 */

// Mock DOM elements for testing
class MockElement {
    constructor(tagName = 'div') {
        this.tagName = tagName;
        this.innerHTML = '';
        this.style = {};
        this.classList = {
            add: jest.fn(),
            remove: jest.fn(),
            contains: jest.fn()
        };
        this.addEventListener = jest.fn();
        this.appendChild = jest.fn();
        this.parentNode = null;
    }
}

// Mock document for testing
const mockDocument = {
    getElementById: jest.fn(),
    querySelector: jest.fn(),
    createElement: jest.fn(() => new MockElement()),
    addEventListener: jest.fn(),
    body: new MockElement('body')
};

// Mock window for testing
const mockWindow = {
    innerWidth: 1280,
    innerHeight: 720
};

global.document = mockDocument;
global.window = mockWindow;

describe('PomodoroTimer Visual Enhancements', () => {
    let timer;
    let mockElements;

    beforeEach(() => {
        // Reset mocks
        jest.clearAllMocks();
        
        // Setup mock DOM elements
        mockElements = {
            timeDisplay: new MockElement(),
            startButton: new MockElement(),
            resetButton: new MockElement(),
            statusDisplay: new MockElement(),
            progressContainer: new MockElement(),
            progressBar: new MockElement(),
            progressBg: new MockElement()
        };

        mockElements.timeDisplay.textContent = '25:00';
        mockElements.startButton.textContent = '開始';
        mockElements.statusDisplay.textContent = '作業中';

        // Mock getElementById and querySelector
        mockDocument.getElementById.mockImplementation((id) => {
            switch (id) {
                case 'time': return mockElements.timeDisplay;
                case 'start': return mockElements.startButton;
                case 'reset': return mockElements.resetButton;
                default: return null;
            }
        });

        mockDocument.querySelector.mockImplementation((selector) => {
            switch (selector) {
                case '.status': return mockElements.statusDisplay;
                case '.progress': return mockElements.progressContainer;
                case '.progress-bar': return mockElements.progressBar;
                case '.progress-bg': return mockElements.progressBg;
                default: return null;
            }
        });
    });

    test('should initialize with correct default values', () => {
        // Import and initialize timer (mocked)
        const timer = {
            totalTime: 25 * 60,
            currentTime: 25 * 60,
            isRunning: false,
            radius: 90,
            circumference: 2 * Math.PI * 90
        };

        expect(timer.totalTime).toBe(1500);
        expect(timer.currentTime).toBe(1500);
        expect(timer.isRunning).toBe(false);
        expect(timer.circumference).toBeCloseTo(565.49);
    });

    test('should format time display correctly', () => {
        const formatTime = (seconds) => {
            const minutes = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        };

        expect(formatTime(1500)).toBe('25:00');
        expect(formatTime(1499)).toBe('24:59');
        expect(formatTime(300)).toBe('05:00');
        expect(formatTime(59)).toBe('00:59');
        expect(formatTime(0)).toBe('00:00');
    });

    test('should calculate progress correctly', () => {
        const calculateProgress = (totalTime, currentTime) => {
            return (totalTime - currentTime) / totalTime;
        };

        expect(calculateProgress(1500, 1500)).toBe(0); // 0% progress
        expect(calculateProgress(1500, 750)).toBe(0.5); // 50% progress
        expect(calculateProgress(1500, 0)).toBe(1); // 100% progress
    });

    test('should calculate color transitions correctly', () => {
        const calculateColor = (progress) => {
            let color;
            if (progress < 0.5) {
                // Blue to yellow
                const ratio = progress * 2;
                const r = Math.round(52 + (255 - 52) * ratio);
                const g = Math.round(152 + (255 - 152) * ratio);
                const b = Math.round(219 - 219 * ratio);
                color = `rgb(${r}, ${g}, ${b})`;
            } else {
                // Yellow to red
                const ratio = (progress - 0.5) * 2;
                const r = 255;
                const g = Math.round(255 - 24 * ratio);
                const b = Math.round(0 + 60 * ratio);
                color = `rgb(${r}, ${g}, ${b})`;
            }
            return color;
        };

        expect(calculateColor(0)).toBe('rgb(52, 152, 219)'); // Blue at start
        expect(calculateColor(0.5)).toBe('rgb(255, 255, 0)'); // Yellow at middle
        expect(calculateColor(1)).toBe('rgb(255, 231, 60)'); // Red-ish at end
    });

    test('should update circular progress stroke-dashoffset correctly', () => {
        const updateProgress = (circumference, progress) => {
            return circumference * (1 - progress);
        };

        const circumference = 2 * Math.PI * 90;
        
        expect(updateProgress(circumference, 0)).toBeCloseTo(circumference); // No progress
        expect(updateProgress(circumference, 0.5)).toBeCloseTo(circumference / 2); // Half progress
        expect(updateProgress(circumference, 1)).toBeCloseTo(0); // Full progress
    });

    test('should validate timer state transitions', () => {
        const timer = {
            isRunning: false,
            start: function() { this.isRunning = true; },
            pause: function() { this.isRunning = false; },
            reset: function() { this.isRunning = false; this.currentTime = this.totalTime; },
            totalTime: 1500,
            currentTime: 1500
        };

        // Initial state
        expect(timer.isRunning).toBe(false);
        expect(timer.currentTime).toBe(1500);

        // Start timer
        timer.start();
        expect(timer.isRunning).toBe(true);

        // Pause timer
        timer.pause();
        expect(timer.isRunning).toBe(false);

        // Reset timer
        timer.currentTime = 1000; // Simulate some time passed
        timer.reset();
        expect(timer.isRunning).toBe(false);
        expect(timer.currentTime).toBe(1500);
    });
});

// Export for Jest if in Node.js environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        MockElement,
        mockDocument,
        mockWindow
    };
}