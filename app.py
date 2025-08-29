from flask import Flask, render_template, jsonify, request
from services.progress_manager import ProgressManager

app = Flask(__name__)

# Initialize progress manager
progress_manager = ProgressManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current progress data"""
    try:
        progress_data = progress_manager.get_progress()
        return jsonify({
            "success": True,
            "data": progress_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/progress', methods=['POST'])
def update_progress():
    """Update progress data"""
    try:
        data = request.get_json()
        if data is None:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        # Handle different types of updates
        if data.get('action') == 'complete_session':
            focus_time = data.get('focus_time', 25)
            progress_data = progress_manager.add_completed_session(focus_time)
        elif data.get('action') == 'reset_today':
            progress_data = progress_manager.reset_today_progress()
        else:
            # General update
            progress_data = progress_manager.update_progress(data)
        
        return jsonify({
            "success": True,
            "data": progress_data
        })
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": "Invalid JSON data"
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
