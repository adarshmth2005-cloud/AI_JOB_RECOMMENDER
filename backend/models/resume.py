from datetime import datetime
from extensions import db


class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.String(50), unique=True, nullable=True)
    filename = db.Column(db.String(255), nullable=True)
    extracted_text = db.Column(db.Text, nullable=True)
    resume_html = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "dataset_id": self.dataset_id,
            "filename": self.filename,
            "extracted_text": self.extracted_text,
            "resume_html": self.resume_html,
            "category": self.category,
            "skills": self.skills,
            "uploaded_at": self.uploaded_at.isoformat()
            if self.uploaded_at else None
        }