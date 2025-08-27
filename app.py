from flask import Flask, render_template, request, jsonify
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
        progress_data = progress_manager.get_progress()
        return jsonify(progress_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/progress', methods=['POST'])
def update_progress():
    """Update progress data"""
    try:
        # Check if request has JSON content type
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
            
        data = request.get_json()
        
        if data is None:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract parameters from request
        completed_sessions = data.get('completed_sessions')
        total_focus_time = data.get('total_focus_time')
        
        # Check if we should add a completed session instead of updating directly
        if data.get('action') == 'add_session':
            session_duration = data.get('session_duration', 25)
            updated_data = progress_manager.add_completed_session(session_duration)
        elif data.get('action') == 'reset':
            updated_data = progress_manager.reset_progress()
        else:
            # Regular update
            updated_data = progress_manager.update_progress(completed_sessions, total_focus_time)
        
        return jsonify(updated_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
