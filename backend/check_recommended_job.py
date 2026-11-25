from app import app
from models.job import Job
from skills_extractor import extract_skills

with app.app_context():

    job = Job.query.get(103)

    if job:
        print("Job ID:", job.id)
        print("Job Title:", job.title)
        print("Category:", job.category)

        print("\nOriginal Required Skills:")
        print(job.required_skills)

        print("\nExtracted Skills:")
        print(extract_skills(job.required_skills or ""))
    else:
        print("Job not found")