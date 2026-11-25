from app import app
from extensions import db
from models.job import Job
from job_classifier import classify_job

with app.app_context():
    jobs = Job.query.all()

    classified = 0
    unclassified = 0

    for job in jobs:
        category = classify_job(job.title, job.description)

        job.category = category

        if category:
            classified += 1
        else:
            unclassified += 1

        if (classified + unclassified) % 1000 == 0:
            db.session.commit()
            print("Processed:", classified + unclassified)

    db.session.commit()

    print("\nJob Classification Completed!")
    print("Total jobs:", len(jobs))
    print("Classified jobs:", classified)
    print("Unclassified jobs:", unclassified)
