
from flask import Blueprint, request, jsonify

from extensions import db
from models.job import Job


jobs_bp = Blueprint(
    "jobs",
    __name__,
    url_prefix="/api/jobs"
)


# 1. Create Job API
@jobs_bp.route("/", methods=["POST"])
def create_job():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Valid JSON data is required"
            }), 400

        title = data.get("title")
        company = data.get("company")
        description = data.get("description")
        required_skills = data.get("required_skills")

        if not all([title, company, description, required_skills]):
            return jsonify({
                "status": "error",
                "message": "Title, company, description and required_skills are required"
            }), 400

        job = Job(
            title=str(title).strip(),
            company=str(company).strip(),
            description=str(description).strip(),
            required_skills=str(required_skills).strip(),
            location=data.get("location"),
            category=data.get("category")
        )

        db.session.add(job)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Job created successfully",
            "job": job.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 2. Get Jobs with Search, Filters and Pagination
@jobs_bp.route("/", methods=["GET"])
def get_jobs():
    try:
        page = max(request.args.get("page", 1, type=int), 1)

        per_page = min(
            max(request.args.get("per_page", 10, type=int), 1),
            100
        )

        search = request.args.get("search", "").strip()
        category = request.args.get("category", "").strip()
        location = request.args.get("location", "").strip()

        query = Job.query

        if search:
            query = query.filter(
                db.or_(
                    Job.title.ilike(f"%{search}%"),
                    Job.company.ilike(f"%{search}%"),
                    Job.description.ilike(f"%{search}%"),
                    Job.required_skills.ilike(f"%{search}%")
                )
            )

        if category:
            query = query.filter(
                Job.category.ilike(category)
            )

        if location:
            query = query.filter(
                Job.location.ilike(f"%{location}%")
            )

        pagination = query.order_by(
            Job.id.desc()
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return jsonify({
            "status": "success",
            "total_jobs": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total_pages": pagination.pages,
            "jobs": [
                job.to_dict()
                for job in pagination.items
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 3. Get Single Job by ID
@jobs_bp.route("/<int:job_id>", methods=["GET"])
def get_job(job_id):
    try:
        job = db.session.get(Job, job_id)

        if not job:
            return jsonify({
                "status": "error",
                "message": "Job not found"
            }), 404

        return jsonify({
            "status": "success",
            "job": job.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 4. Update Job API
@jobs_bp.route("/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    try:
        job = db.session.get(Job, job_id)

        if not job:
            return jsonify({
                "status": "error",
                "message": "Job not found"
            }), 404

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "status": "error",
                "message": "Valid JSON data is required"
            }), 400

        allowed_fields = [
            "title",
            "company",
            "description",
            "required_skills",
            "location",
            "category"
        ]

        for field in allowed_fields:
            if field in data:
                setattr(job, field, data[field])

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Job updated successfully",
            "job": job.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 5. Delete Job API
@jobs_bp.route("/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    try:
        job = db.session.get(Job, job_id)

        if not job:
            return jsonify({
                "status": "error",
                "message": "Job not found"
            }), 404

        db.session.delete(job)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Job deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 6. Get All Available Job Categories
@jobs_bp.route("/categories", methods=["GET"])
def get_job_categories():
    try:
        categories = db.session.query(
            Job.category
        ).filter(
            Job.category.isnot(None),
            Job.category != ""
        ).distinct().order_by(
            Job.category.asc()
        ).all()

        return jsonify({
            "status": "success",
            "total_categories": len(categories),
            "categories": [
                category[0]
                for category in categories
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 7. Get All Available Job Locations
@jobs_bp.route("/locations", methods=["GET"])
def get_job_locations():
    try:
        locations = db.session.query(
            Job.location
        ).filter(
            Job.location.isnot(None),
            Job.location != ""
        ).distinct().order_by(
            Job.location.asc()
        ).all()

        return jsonify({
            "status": "success",
            "total_locations": len(locations),
            "locations": [
                location[0]
                for location in locations
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
