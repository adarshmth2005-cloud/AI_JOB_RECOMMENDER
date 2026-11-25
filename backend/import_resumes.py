
import csv
import os

from app import app
from extensions import db
from models.resume import Resume

CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "archive",
    "Resume",
    "Resume.csv"
)

CSV_PATH = os.path.abspath(CSV_PATH)

def import_resumes():
    if not os.path.exists(CSV_PATH):
        print("CSV file not found:", CSV_PATH)
        return

    with app.app_context():
        existing_ids = {
            str(row[0])
            for row in db.session.query(Resume.dataset_id)
            .filter(Resume.dataset_id.isnot(None))
            .all()
        }

        imported = 0
        skipped = 0
        batch = []

        with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                dataset_id = str(row.get("ID", "")).strip()

                if not dataset_id or dataset_id in existing_ids:
                    skipped += 1
                    continue

                resume = Resume(
                    dataset_id=dataset_id,
                    filename=None,
                    extracted_text=row.get("Resume_str", ""),
                    resume_html=row.get("Resume_html", ""),
                    category=row.get("Category", ""),
                    skills=""
                )

                batch.append(resume)
                existing_ids.add(dataset_id)

                if len(batch) >= 200:
                    db.session.add_all(batch)
                    db.session.commit()
                    imported += len(batch)
                    batch = []
                    print("Imported:", imported)

        if batch:
            db.session.add_all(batch)
            db.session.commit()
            imported += len(batch)

        print("\nImport completed!")
        print("New resumes imported:", imported)
        print("Duplicate/empty IDs skipped:", skipped)


if __name__ == "__main__":
    try:
        import_resumes()
    except Exception as error:
        db.session.rollback()
        print("Import failed:", error)
