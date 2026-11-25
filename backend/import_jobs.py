
import csv

from app import app
from extensions import db
from models.job import Job


CSV_PATH = r"C:\Users\Adarsh\AI_JOB_RECOMMENDER\archive (1)\job_descriptions.csv"


with app.app_context():

    imported = 0
    skipped = 0

    # Existing jobs ka record check karna
    existing_jobs = {
        (
            job.title.strip().lower(),
            job.company.strip().lower()
        )
        for job in Job.query.all()
    }

    with open(
        CSV_PATH,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            title = (row.get("Job Title") or "").strip()
            company = (row.get("Company") or "").strip()
            description = (row.get("Job Description") or "").strip()
            skills = (row.get("skills") or "").strip()

            location = " - ".join(
                value for value in [
                    (row.get("location") or "").strip(),
                    (row.get("Country") or "").strip()
                ] if value
            )

            if not title or not company:
                skipped += 1
                continue

            # Duplicate check
            job_key = (title.lower(), company.lower())

            if job_key in existing_jobs:
                skipped += 1
                continue

            existing_jobs.add(job_key)

            # New job create karna
            job = Job(
                title=title[:150],
                company=company[:150],
                description=description or "No description available",
                required_skills=skills or "Not specified",
                location=location[:100] or None
            )

            db.session.add(job)
            imported += 1

            if imported % 500 == 0:
                db.session.commit()
                print("Imported:", imported)

    db.session.commit()

    print("\nJob Dataset Import Completed!")
    print("New jobs imported:", imported)
    print("Rows skipped:", skipped)
    print("Total jobs in database:", Job.query.count())

