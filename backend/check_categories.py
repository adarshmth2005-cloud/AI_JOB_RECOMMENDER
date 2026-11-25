
from app import app
from models.resume import Resume
from sqlalchemy import func

with app.app_context():

    results = (
        Resume.query
        .with_entities(
            Resume.category,
            func.count(Resume.id)
        )
        .group_by(Resume.category)
        .all()
    )

    print("\nResume Categories:")
    print("--------------------------")

    for category, count in results:
        print(f"{category}: {count}")

    print("--------------------------")
    print("Total categories:", len(results))
