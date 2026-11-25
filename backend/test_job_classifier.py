
from job_classifier import classify_job

test_jobs = [
    ("HR Manager", "Responsible for recruitment and employee relations"),
    ("Python Developer", "Python, Flask, SQL and software development"),
    ("Financial Analyst", "Financial reporting, accounting and budgeting"),
    ("Graphic Designer", "UI design, Photoshop and creative design"),
    ("Nurse", "Patient care and clinical healthcare services"),
    ("Sales Executive", "Sales, customer acquisition and lead generation"),
    ("Mechanical Engineer", "Mechanical engineering and machine design"),
    ("Teacher", "Teaching students and preparing lesson plans")
]

for title, description in test_jobs:

    category = classify_job(title, description)

    print("Job:", title)
    print("Predicted Category:", category)
    print("----------------------------")
