from flask import Flask, render_template, jsonify, request
from services.progress_manager import ProgressManager

app = Flask(__name__)
progress_manager = ProgressManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress data"""
    try:
        progress = progress_manager.get_progress()
        return jsonify(progress)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/progress', methods=['POST'])
def add_progress():
    """Add a completed pomodoro session"""
    try:
        data = request.get_json() or {}
        focus_time = data.get('focus_time', 25)  # Default 25 minutes
        
        progress = progress_manager.add_completed_session(focus_time)
        return jsonify(progress)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
