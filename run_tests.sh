#!/bin/bash

echo "====================================="
echo "Running Pomodoro Timer Test Suite"
echo "====================================="

echo ""
echo "1. Running Python tests..."
echo "-------------------------------------"
python -m pytest tests/ -v

echo ""
echo "2. Running JavaScript tests..."
echo "-------------------------------------"
npm test

echo ""
echo "3. Testing Flask app functionality..."
echo "-------------------------------------"
python -c "
from app import app
import json

# Test the app in test mode
app.config['TESTING'] = True
client = app.test_client()

# Test main page
response = client.get('/')
print('✓ Main page loads successfully' if response.status_code == 200 else '✗ Main page failed')

# Test progress API
response = client.get('/api/progress')
if response.status_code == 200:
    data = response.get_json()
    print('✓ Progress API GET works:', data)
else:
    print('✗ Progress API GET failed')

# Test posting progress
response = client.post('/api/progress', 
                      data=json.dumps({'session_duration': 25}),
                      content_type='application/json')
if response.status_code == 200:
    data = response.get_json()
    print('✓ Progress API POST works:', data)
else:
    print('✗ Progress API POST failed')
"

echo ""
echo "====================================="
echo "All tests completed!"
echo "====================================="