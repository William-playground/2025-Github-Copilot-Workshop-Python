# Pomodoro Timer Test Documentation

## Overview

This document describes the comprehensive test suite for the Pomodoro Timer web application, implemented as part of Step 7 (テストの追加).

## Test Coverage

### Python Backend Tests

Located in `tests/` directory:

#### `tests/test_app.py`
- Tests Flask application routes
- Tests API endpoints (`/api/progress` GET/POST)
- Validates response formats and status codes

#### `tests/test_progress_manager.py`
- Tests progress data management logic
- Tests session tracking and persistence
- Tests data file operations and error handling
- Tests edge cases and invalid data recovery

### JavaScript Frontend Tests

Located in `static/js/timer.test.js`:

#### TimerUtils Tests
- Time formatting functions
- Progress calculation utilities
- Input validation functions

#### PomodoroTimer Class Tests
- Timer initialization and state management
- DOM element interaction
- Timer controls (start/stop/reset)
- Progress tracking and API communication
- Session completion workflow

## Testing Frameworks

### Python
- **pytest**: Main testing framework
- **unittest**: Built-in Python testing for compatibility
- Coverage: 12 tests covering all backend logic

### JavaScript
- **Jest**: Main testing framework
- **JSDOM**: DOM simulation for browser environment
- Coverage: 21 tests covering timer logic and UI interactions

## Running Tests

### All Tests
```bash
./run_tests.sh
```

### Python Tests Only
```bash
python -m pytest tests/ -v
```
or
```bash
npm run test:python
```

### JavaScript Tests Only
```bash
npm test
```
or
```bash
npm run test:js
```

## Test Structure

### Backend Test Architecture
- Uses dependency injection for testable progress manager
- Temporary files for isolated test data
- Mock-friendly API design with consistent JSON responses

### Frontend Test Architecture
- JSDOM for DOM simulation without browser
- Mocked fetch API for testing network requests
- Graceful handling of missing DOM elements in tests

## Key Test Features

### Backend
- Data persistence testing across instances
- Error recovery and invalid data handling
- Session duration customization
- Date-based progress tracking

### Frontend
- Timer state management
- UI element updates
- API communication error handling
- Progress display updates
- Session completion workflow

## Dependencies

### Python
- Flask (web framework)
- pytest (testing)

### JavaScript
- Jest (testing framework)
- JSDOM (DOM simulation)
- jest-environment-jsdom (Jest environment)

## Files Structure

```
tests/
├── test_app.py                 # Flask app tests
└── test_progress_manager.py    # Progress logic tests

static/js/
├── timer.js                    # Main timer logic
└── timer.test.js              # Timer tests

jest.config.json               # Jest configuration
jest.setup.js                 # Jest setup for TextEncoder
run_tests.sh                  # Comprehensive test runner
```

## Test Quality Assurance

All tests are designed to:
- Be independent and isolated
- Handle edge cases and error conditions
- Provide clear assertions and error messages
- Use proper mocking for external dependencies
- Maintain consistency with the existing codebase