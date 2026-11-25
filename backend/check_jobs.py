
from app import app
from models.job import Job

with app.app_context():

    total_jobs = Job.query.count()

    print("\n===== JOB DATABASE REPORT =====")
    print("Total Jobs:", total_jobs)

    print("\n===== FIRST 10 JOBS =====")

    jobs = Job.query.limit(10).all()

    for job in jobs:
        print("-----------------------------")
        print("Job ID:", job.id)
        print("Title:", job.title)
        print("Company:", job.company)
        print("Location:", job.location)
        print("Required Skills:", job.required_skills)
