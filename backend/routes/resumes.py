
import os
import uuid

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    send_from_directory
)
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader

from extensions import db
from models.resume import Resume
from models.job import Job
from skills_extractor import clean_resume_text, extract_skills


resume_bp = Blueprint(
    "resumes",
    __name__,
    url_prefix="/api/resumes"
)

ALLOWED_EXTENSIONS = {"pdf"}


# Resume category classifier
def classify_resume_category(text):
    text = (text or "").lower()

    categories = {
        "INFORMATION-TECHNOLOGY": [
            "python", "java", "programming", "software",
            "developer", "javascript", "react", "database"
        ],
        "HR": [
            "human resources", "recruitment", "talent acquisition",
            "employee relations", "hr"
        ],
        "DESIGNER": [
            "graphic design", "photoshop", "illustrator",
            "ui design", "ux design", "figma"
        ],
        "TEACHER": [
            "teaching", "teacher", "education", "classroom",
            "lesson planning"
        ],
        "ADVOCATE": [
            "lawyer", "legal", "advocate", "litigation",
            "court"
        ],
        "BUSINESS-DEVELOPMENT": [
            "business development", "client acquisition",
            "sales strategy", "business growth"
        ],
        "HEALTHCARE": [
            "healthcare", "nursing", "medical", "patient care",
            "hospital"
        ],
        "FITNESS": [
            "fitness", "personal trainer", "gym", "nutrition"
        ],
        "AGRICULTURE": [
            "agriculture", "farming", "agronomy", "crop"
        ],
        "BPO": [
            "bpo", "customer support", "call center",
            "voice process"
        ],
        "SALES": [
            "sales", "sales executive", "lead generation",
            "customer relationship"
        ],
        "CONSULTANT": [
            "consultant", "consulting", "business analysis"
        ],
        "DIGITAL-MEDIA": [
            "digital marketing", "social media", "seo",
            "content marketing"
        ],
        "AUTOMOBILE": [
            "automobile", "automotive", "vehicle",
            "mechanical automobile"
        ],
        "CHEF": [
            "chef", "cooking", "food preparation",
            "kitchen"
        ],
        "FINANCE": [
            "finance", "financial analysis", "investment",
            "banking", "financial planning"
        ],
        "APPAREL": [
            "apparel", "fashion", "garment", "textile"
        ],
        "ENGINEERING": [
            "engineering", "mechanical", "civil engineering",
            "electrical engineering"
        ],
        "ACCOUNTANT": [
            "accountant", "accounting", "bookkeeping",
            "taxation"
        ],
        "CONSTRUCTION": [
            "construction", "site engineer", "building",
            "project construction"
        ],
        "PUBLIC-RELATIONS": [
            "public relations", "media relations",
            "communication"
        ],
        "BANKING": [
            "banking", "bank operations", "loan processing"
        ],
        "ARTS": [
            "arts", "artist", "painting", "creative arts"
        ],
        "AVIATION": [
            "aviation", "pilot", "aircraft", "airport"
        ]
    }

    best_category = None
    best_score = 0

    for category, keywords in categories.items():
        score = sum(
            1 for keyword in keywords
            if keyword in text
        )

        if score > best_score:
            best_score = score
            best_category = category

    return best_category or "OTHER"


# Check file extension
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# 1. Upload Resume API
@resume_bp.route("/upload", methods=["POST"])
def upload_resume():
    try:
        if "resume" not in request.files:
            return jsonify({
                "status": "error",
                "message": "Please select a PDF resume"
            }), 400

        file = request.files["resume"]

        if not file or file.filename == "":
            return jsonify({
                "status": "error",
                "message": "No file selected"
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "status": "error",
                "message": "Only PDF files are allowed"
            }), 400

        original_filename = secure_filename(file.filename)

        if not original_filename:
            return jsonify({
                "status": "error",
                "message": "Invalid filename"
            }), 400

        upload_folder = os.path.join(
            current_app.root_path,
            "uploads"
        )

        os.makedirs(upload_folder, exist_ok=True)

        unique_filename = (
            str(uuid.uuid4())
            + "_"
            + original_filename
        )

        file_path = os.path.join(
            upload_folder,
            unique_filename
        )

        file.save(file_path)

        try:
            reader = PdfReader(file_path)

            extracted_text = ""

            for page in reader.pages:
                extracted_text += (page.extract_text() or "") + "\n"

            extracted_text = clean_resume_text(extracted_text)

        except Exception:
            if os.path.exists(file_path):
                os.remove(file_path)

            return jsonify({
                "status": "error",
                "message": "Unable to read this PDF. Please upload a valid PDF."
            }), 400

        if not extracted_text.strip():
            if os.path.exists(file_path):
                os.remove(file_path)

            return jsonify({
                "status": "error",
                "message": "No readable text found in PDF. Scanned PDFs may require OCR."
            }), 400

        skills = extract_skills(extracted_text)
        category = classify_resume_category(extracted_text)

        resume = Resume(
            filename=unique_filename,
            extracted_text=extracted_text,
            category=category,
            skills=", ".join(skills)
        )

        db.session.add(resume)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Resume uploaded successfully",
            "resume": {
                "id": resume.id,
                "filename": resume.filename,
                "category": resume.category,
                "skills": skills
            }
        }), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 2. Get Resumes with Search and Cursor Pagination
@resume_bp.route("/", methods=["GET"])
def get_resumes():
    try:
        limit = request.args.get("limit", 50, type=int)
        limit = min(max(limit or 50, 1), 100)

        cursor = request.args.get("cursor", type=int)
        search = (request.args.get("search") or "").strip()

        # Base query
        query = Resume.query

        # Search by filename or exact resume ID
        if search:
            search_pattern = f"%{search}%"

            search_conditions = [
                Resume.filename.ilike(search_pattern)
            ]

            if search.isdigit():
                search_conditions.append(
                    Resume.id == int(search)
                )

            query = query.filter(
                or_(*search_conditions)
            )

        # Count matching resumes
        total_resumes = query.count()

        # Cursor pagination
        if cursor:
            query = query.filter(
                Resume.id < cursor
            )

        records = query.order_by(
            Resume.id.desc()
        ).limit(limit + 1).all()

        has_more = len(records) > limit
        resumes = records[:limit]

        next_cursor = (
            resumes[-1].id
            if has_more and resumes
            else None
        )

        return jsonify({
            "status": "success",
            "total_resumes": total_resumes,
            "loaded_resumes": len(resumes),
            "has_more": has_more,
            "next_cursor": next_cursor,
            "resumes": [
                {
                    "id": resume.id,
                    "filename": resume.filename,
                    "category": resume.category,
                    "uploaded_at": (
                        resume.uploaded_at.isoformat()
                        if resume.uploaded_at else None
                    )
                }
                for resume in resumes
            ]
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 3. Get Resume Analysis
@resume_bp.route("/<int:resume_id>/analysis", methods=["GET"])
def analyze_resume(resume_id):
    try:
        resume = db.session.get(Resume, resume_id)

        if not resume:
            return jsonify({
                "status": "error",
                "message": "Resume not found"
            }), 404

        skills = extract_skills(
            resume.extracted_text or ""
        )

        return jsonify({
            "status": "success",
            "analysis": {
                "id": resume.id,
                "filename": resume.filename,
                "category": resume.category,
                "skills": skills,
                "text_length": len(
                    resume.extracted_text or ""
                ),
                "extracted_text": resume.extracted_text or ""
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 4. Get Matched and Missing Skills for a Job
@resume_bp.route(
    "/<int:resume_id>/missing-skills/<int:job_id>",
    methods=["GET"]
)
def get_missing_skills(resume_id, job_id):
    try:
        resume = db.session.get(Resume, resume_id)
        job = db.session.get(Job, job_id)

        if not resume:
            return jsonify({
                "status": "error",
                "message": "Resume not found"
            }), 404

        if not job:
            return jsonify({
                "status": "error",
                "message": "Job not found"
            }), 404

        resume_skills = {
            skill.lower()
            for skill in extract_skills(
                resume.extracted_text or ""
            )
        }

        job_skills = {
            skill.lower()
            for skill in extract_skills(
                job.required_skills or ""
            )
        }

        matched_skills = sorted(
            resume_skills.intersection(job_skills)
        )

        missing_skills = sorted(
            job_skills - resume_skills
        )

        return jsonify({
            "status": "success",
            "resume_id": resume_id,
            "job_id": job_id,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# 5. View Original Resume PDF
@resume_bp.route("/<int:resume_id>/file", methods=["GET"])
def get_resume_file(resume_id):
    try:
        resume = db.session.get(Resume, resume_id)

        if not resume:
            return jsonify({
                "status": "error",
                "message": "Resume not found"
            }), 404

        if not resume.filename:
            return jsonify({
                "status": "error",
                "message": (
                    "Original PDF is not available for this resume. "
                    "It may have been imported from the CSV dataset."
                )
            }), 404

        upload_folder = os.path.join(
            current_app.root_path,
            "uploads"
        )

        file_path = os.path.join(
            upload_folder,
            resume.filename
        )

        if not os.path.isfile(file_path):
            return jsonify({
                "status": "error",
                "message": (
                    "PDF file is missing. "
                    "Resume analysis data is still available."
                )
            }), 404

        return send_from_directory(
            upload_folder,
            resume.filename,
            mimetype="application/pdf",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
