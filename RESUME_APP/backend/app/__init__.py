from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder=None)
    CORS(app)
    
    # Configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from backend.app.routes import upload, matching, recommendations, interview, career, cover_letter, analytics, export
    
    app.register_blueprint(upload.bp)
    app.register_blueprint(matching.bp)
    app.register_blueprint(recommendations.bp)
    app.register_blueprint(interview.bp)
    app.register_blueprint(career.bp)
    app.register_blueprint(cover_letter.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(export.bp)
    
    # Serve frontend files
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend')
    
    @app.route('/')
    def index():
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        if os.path.exists(os.path.join(frontend_path, path)):
            return send_from_directory(frontend_path, path)
        return send_from_directory(frontend_path, 'index.html')
    
    return app

# Note: Use run.py from project root instead of running this directly
if __name__ == '__main__':
    import sys
    import os
    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, project_root)
    
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"\n✅ Career Assistant starting on http://localhost:{port}\n")
    app.run(debug=True, host='0.0.0.0', port=port)

