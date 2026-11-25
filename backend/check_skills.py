
from app import app
from models.resume import Resume

with app.app_context():

    resume = Resume.query.get(3)

    if resume:
        print("Resume ID:", resume.id)
        print("Category:", resume.category)
        print("\nExtracted Skills:")
        print(resume.skills)
    else:
        print("Resume not found")
