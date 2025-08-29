from flask import Flask, render_template, jsonify, request
from services.progress_manager import ProgressManager

app = Flask(__name__)
progress_manager = ProgressManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress data."""
    try:
        data = progress_manager.get_progress()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/progress', methods=['POST'])
def update_progress():
    """Update progress data."""
    try:
        updates = request.get_json(force=True)
        if not updates:
            return jsonify({"error": "No data provided"}), 400
        
        data = progress_manager.update_progress(updates)
        return jsonify(data)
    except Exception as e:
        if "Bad Request" in str(e):
            return jsonify({"error": "No data provided"}), 400
        return jsonify({"error": str(e)}), 500

@app.route('/api/complete', methods=['POST'])
def complete_session():
    """Record a completed Pomodoro session."""
    try:
        request_data = request.get_json() or {}
        focus_time = request_data.get('focus_time_minutes', 25)
        
        data = progress_manager.complete_session(focus_time)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
