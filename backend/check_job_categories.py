from app import app
from models.job import Job
from sqlalchemy import func

with app.app_context():
    results = (
        Job.query
        .with_entities(Job.category, func.count(Job.id))
        .group_by(Job.category)
        .order_by(func.count(Job.id).desc())
        .all()
    )

    print("\nJob Category Report")
    print("-----------------------------")

    for category, count in results:
        print(f"{category or 'Unclassified'}: {count}")

    print("\nTotal categories:", len(results))