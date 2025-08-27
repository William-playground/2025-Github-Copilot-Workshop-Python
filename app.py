from flask import Flask, render_template, jsonify, request
from services.gamification_manager import GamificationManager

app = Flask(__name__)
gamification = GamificationManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/progress', methods=['GET'])
def get_progress():
    """Get current user progress and gamification data"""
    return jsonify(gamification.get_progress())

@app.route('/api/progress/complete', methods=['POST'])
def complete_pomodoro():
    """Record a completed Pomodoro session"""
    data = request.get_json() or {}
    focus_minutes = data.get('focus_minutes', 25)
    
    result = gamification.complete_pomodoro(focus_minutes)
    return jsonify(result)

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics for a specified period"""
    period = request.args.get('period', 'week')
    return jsonify(gamification.get_statistics(period))

@app.route('/api/achievements', methods=['GET'])
def get_achievements():
    """Get all achievements (locked and unlocked)"""
    achievements = []
    for ach in gamification.progress.achievements:
        ach_dict = {
            'id': ach.id,
            'name': ach.name,
            'description': ach.description,
            'icon': ach.icon,
            'unlocked': ach.unlocked,
            'unlocked_at': ach.unlocked_at
        }
        achievements.append(ach_dict)
    
    return jsonify(achievements)

if __name__ == '__main__':
    app.run(debug=True)
