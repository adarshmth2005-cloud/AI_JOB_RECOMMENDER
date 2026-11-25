
from flask import Blueprint, jsonify, request

from extensions import db
from models.resume import Resume
from models.job import Job
from recommendation import recommend_jobs


recommendation_bp = Blueprint(
    "recommendations",
    __name__,
    url_prefix="/api/recommendations"
)


@recommendation_bp.route("/<int:resume_id>", methods=["GET"])
def get_recommendations(resume_id):

    try:
        resume = db.session.get(Resume, resume_id)

        if not resume:
            return jsonify({
                "status": "error",
                "message": "Resume not found"
            }), 404

        # Filters
        category = request.args.get("category", "").strip()
        location = request.args.get("location", "").strip()

        # Pagination
        page = request.args.get("page", 1, type=int) or 1
        per_page = request.args.get("per_page", 50, type=int) or 50

        page = max(page, 1)
        per_page = max(1, min(per_page, 100))

        # Job query
        query = Job.query

        if category:
            query = query.filter(
                Job.category.ilike(category)
            )

        if location:
            query = query.filter(
                Job.location.ilike(f"%{location}%")
            )

        # Process jobs in batches
        batch_size = 1000
        last_id = 0
        recommendations = []

        while True:

            jobs = query.filter(
                Job.id > last_id
            ).order_by(
                Job.id.asc()
            ).limit(batch_size).all()

            if not jobs:
                break

            last_id = jobs[-1].id

            batch_recommendations = recommend_jobs(
                resume.extracted_text or "",
                jobs,
                resume.category
            )

            recommendations.extend(batch_recommendations)

        # Sort all recommendations
        recommendations.sort(
            key=lambda item: (
                item["skill_match_percentage"],
                item["job_id"]
            ),
            reverse=True
        )

        # Count category-wise jobs
        level_counts = {
            "Basic": 0,
            "Intermediate": 0,
            "Advanced": 0
        }

        for job in recommendations:
            level_counts[job["match_level"]] += 1

        total_recommendations = len(recommendations)

        # Pagination
        start = (page - 1) * per_page
        end = start + per_page

        paginated_recommendations = recommendations[start:end]

        total_pages = (
            (total_recommendations + per_page - 1) // per_page
        )

        return jsonify({
            "status": "success",
            "resume_id": resume.id,
            "resume_category": resume.category,
            "minimum_skill_match": 0,
            "level_counts": level_counts,
            "total_recommendations": total_recommendations,
            "current_page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "has_more": page < total_pages,
            "recommendations": paginated_recommendations
        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
