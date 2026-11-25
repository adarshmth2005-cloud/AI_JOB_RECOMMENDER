
from app import app
from models.job import Job

with app.app_context():
    total_jobs = Job.query.count()

    print("Total jobs in database:", total_jobs)
