from flask import Flask, render_template, jsonify, request
from services.progress_manager import ProgressManager

app = Flask(__name__)

# 進捗管理インスタンス
progress_manager = ProgressManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """進捗データ取得API"""
    try:
        progress_data = progress_manager.get_today_progress()
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
def save_progress():
    """進捗データ保存API"""
    try:
        data = request.get_json()
        focus_minutes = data.get('focus_minutes', 25)
        
        progress_data = progress_manager.add_completed_session(focus_minutes)
        return jsonify({
            "success": True,
            "data": progress_data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
