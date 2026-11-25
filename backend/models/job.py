
from datetime import datetime

from extensions import db


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    company = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    required_skills = db.Column(
        db.Text,
        nullable=False
    )

    category = db.Column(
        db.String(100),
        nullable=True,
        index=True
    )

    location = db.Column(
        db.String(100),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):

        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "description": self.description,
            "required_skills": self.required_skills,
            "category": self.category,
            "location": self.location,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            )
        }
