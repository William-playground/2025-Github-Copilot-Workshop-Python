# Testing Guide

This project includes comprehensive testing for both backend (Python/Flask) and frontend (JavaScript) logic.

## Backend Tests (Python)

### Running Tests

```bash
# Run all Python tests with pytest
python -m pytest tests/ -v

# Run specific test files
python -m pytest tests/test_progress_manager.py -v
python -m pytest tests/test_api.py -v

# Run with unittest
python -m unittest discover tests -v

# Run original basic test
python test_app.py
```

### Test Coverage

**Progress Manager Service Tests** (`tests/test_progress_manager.py`):
- Progress data initialization and persistence
- Adding completed Pomodoro sessions
- Resetting daily progress
- Data file corruption recovery
- Daily counter reset logic

**API Endpoint Tests** (`tests/test_api.py`):
- GET `/api/progress` - retrieving progress data
- POST `/api/progress` - updating progress data
- Session completion API calls
- Error handling for invalid data
- Multiple session tracking

## Frontend Tests (JavaScript)

### Running Tests

```bash
# Run JavaScript tests with Jest
npm test

# Run tests with coverage
npm test -- --coverage
```

### Test Coverage

**Timer Logic Tests** (`tests/timer.test.js`):
- Timer initialization and state management
- Start/pause/reset functionality
- Countdown logic and display updates
- Work/break session switching
- Progress bar updates
- API communication
- Button state management
- Session completion flow

## Test Structure

```
tests/
├── __init__.py                # Python test package
├── setup.js                   # Jest setup for DOM testing
├── test_progress_manager.py   # Backend service tests
├── test_api.py               # API endpoint tests
└── timer.test.js             # Frontend logic tests
```

## Dependencies

**Python Testing:**
- pytest 8.4.1
- unittest (built-in)
- Flask testing client

**JavaScript Testing:**
- Jest with jsdom environment
- Mock DOM setup for testing timer functionality

## Configuration

- `jest.config.json` - Jest configuration for JavaScript tests
- `pytest` automatically discovers tests in `tests/` directory
- `.gitignore` excludes test artifacts and `node_modules`