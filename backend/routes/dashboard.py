
from flask import Blueprint, jsonify

from extensions import db
from models.resume import Resume
from models.job import Job


dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)


# 1. Dashboard Statistics
@dashboard_bp.route("/stats", methods=["GET"])
def get_dashboard_stats():
    try:
        total_resumes = Resume.query.count()
        total_jobs = Job.query.count()

        resume_categories = db.session.query(
            Resume.category,
            db.func.count(Resume.id)
        ).filter(
            Resume.category.isnot(None),
            Resume.category != ""
        ).group_by(
            Resume.category
        ).all()

        job_categories = db.session.query(
            Job.category,
            db.func.count(Job.id)
        ).filter(
            Job.category.isnot(None),
            Job.category != ""
        ).group_by(
            Job.category
        ).all()

        return jsonify({
            "status": "success",
            "statistics": {
                "total_resumes": total_resumes,
                "total_jobs": total_jobs,
                "resume_categories": [
                    {
                        "category": category,
                        "count": count
                    }
                    for category, count in resume_categories
                ],
                "job_categories": [
                    {
                        "category": category,
                        "count": count
                    }
                    for category, count in job_categories
                ]
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 2. Recent Resumes
@dashboard_bp.route("/recent-resumes", methods=["GET"])
def get_recent_resumes():
    try:
        resumes = Resume.query.order_by(
            Resume.id.desc()
        ).limit(5).all()

        return jsonify({
            "status": "success",
            "recent_resumes": [
                resume.to_dict()
                for resume in resumes
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 3. Recent Jobs
@dashboard_bp.route("/recent-jobs", methods=["GET"])
def get_recent_jobs():
    try:
        jobs = Job.query.order_by(
            Job.id.desc()
        ).limit(5).all()

        return jsonify({
            "status": "success",
            "recent_jobs": [
                job.to_dict()
                for job in jobs
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
