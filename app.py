from flask import Flask, render_template, jsonify, request
from services.progress_manager import ProgressManager

app = Flask(__name__)
progress_manager = ProgressManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get today's progress data."""
    try:
        progress = progress_manager.get_today_progress()
        return jsonify(progress)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/progress', methods=['POST'])
def save_progress():
    """Save a completed Pomodoro session."""
    try:
        data = request.get_json() or {}
        session_duration = data.get('session_duration', 25)
        progress = progress_manager.add_completed_session(session_duration)
        return jsonify(progress)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
