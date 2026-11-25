
from app import app
from extensions import db
from models.resume import Resume
from skills_extractor import extract_skills

with app.app_context():

    resumes = Resume.query.all()

    total = 0

    for resume in resumes:

        resume_text = resume.extracted_text or ""

        skills = extract_skills(resume_text)

        resume.skills = ", ".join(skills)

        total += 1

        if total % 100 == 0:
            db.session.commit()
            print("Processed resumes:", total)

    db.session.commit()

    print("\nSkills extraction completed!")
    print("Total resumes processed:", total)

