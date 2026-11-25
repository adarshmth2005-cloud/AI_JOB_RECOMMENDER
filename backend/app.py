
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
import os

from config import Config
from extensions import db

# Database Models
from models.job import Job
from models.resume import Resume
from models.user import User

# API Routes
from routes.jobs import jobs_bp
from routes.resumes import resume_bp
from routes.recommendations import recommendation_bp
from routes.dashboard import dashboard_bp
from routes.auth import auth_bp

migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)

    # Initialize migrations
    migrate.init_app(app, db)

    # Create uploads folder
    upload_folder = os.path.join(app.root_path, "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    # Enable frontend-backend communication
    CORS(app)

    # Register API blueprints
    app.register_blueprint(jobs_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)

    # Home API
    @app.route("/")
    def home():
        return jsonify({
            "message": "AI Resume Analysis and Job Recommendation API is running",
            "status": "success"
        }), 200

    # Health Check API
    @app.route("/api/health")
    def health_check():
        return jsonify({
            "status": "success",
            "message": "Backend is healthy"
        }), 200

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    )
