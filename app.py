from flask import Flask, render_template, jsonify, request
from services.config import get_config
from services.repositories import FileProgressRepository, InMemoryProgressRepository
from services.progress_manager import PomodoroProgressManager
from services.interfaces import ProgressManager


def create_app(config_name: str = None, progress_manager: ProgressManager = None):
    """Application factory with dependency injection."""
    app = Flask(__name__)
    
    # Load configuration
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    
    # Dependency injection for progress manager
    if progress_manager is None:
        if app.config['TESTING']:
            repository = InMemoryProgressRepository()
        else:
            repository = FileProgressRepository(app.config['DATA_FILE_PATH'])
        progress_manager = PomodoroProgressManager(repository)
    
    # Store progress manager in app context for route access
    app.progress_manager = progress_manager
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/api/progress', methods=['GET'])
    def get_progress():
        """Get current progress data."""
        try:
            progress = app.progress_manager.get_daily_progress()
            return jsonify(progress)
        except Exception as e:
            return jsonify({'error': 'Failed to get progress data'}), 500
    
    @app.route('/api/progress', methods=['POST'])
    def update_progress():
        """Update progress data."""
        try:
            # Check content type first
            if not request.is_json:
                return jsonify({'error': 'No data provided'}), 400
                
            data = request.get_json()
            if data is None:
                return jsonify({'error': 'No data provided'}), 400
            
            action = data.get('action')
            if action == 'complete_session':
                session_duration = data.get('duration_minutes', 25)
                progress = app.progress_manager.add_completed_session(session_duration)
                return jsonify(progress)
            elif action == 'reset':
                progress = app.progress_manager.reset_daily_progress()
                return jsonify(progress)
            else:
                return jsonify({'error': 'Invalid action'}), 400
        except Exception as e:
            return jsonify({'error': 'Failed to update progress data'}), 500
    
    return app


# Create app instance for direct execution
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
