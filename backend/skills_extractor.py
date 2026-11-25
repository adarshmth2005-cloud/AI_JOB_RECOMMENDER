
import re

SKILLS_LIST = [
    "Python", "Java", "C++", "C", "C#", "JavaScript",
    "TypeScript", "React", "Angular", "HTML", "CSS",
    "Node.js", "PHP", "Flask", "Django", "Spring Boot",
    "REST API", "Git", "GitHub",
    "SQL", "MySQL", "PostgreSQL", "MongoDB",
    "Excel", "Advanced Excel", "Power BI", "Tableau",
    "Pandas", "NumPy", "Matplotlib", "TensorFlow",
    "PyTorch", "Machine Learning", "Deep Learning",
    "Data Science", "Data Analysis", "Statistics",
    "Data Mining", "Data Structures",
    "AWS", "Azure", "Google Cloud", "Docker",
    "Kubernetes", "Linux", "Cybersecurity",
    "Networking", "DevOps",
    "Recruitment", "Talent Acquisition",
    "Human Resource Management", "Human Resources",
    "Employee Relations", "Payroll",
    "Performance Management", "Training and Development",
    "Leadership", "Team Management", "Project Management",
    "Talent Sourcing", "Interviewing", "Onboarding",
    "Recruitment Strategies", "HR Software",
    "Applicant Tracking System", "Workforce Planning",
    "Compensation and Benefits", "Employee Engagement",
    "Labor Law", "HR Analytics",
    "Accounting", "Financial Analysis",
    "Financial Reporting", "Bookkeeping",
    "Taxation", "Auditing", "Budgeting",
    "Financial Planning", "QuickBooks", "Tally", "SAP",
    "Digital Marketing", "SEO", "SEM",
    "Social Media Marketing", "Content Marketing",
    "Content Creation", "Google Analytics",
    "Email Marketing", "Market Research",
    "Sales", "Lead Generation",
    "Customer Relationship Management",
    "Patient Care", "Clinical Research",
    "Medical Coding", "Medical Terminology",
    "Healthcare Management", "Nursing",
    "AutoCAD", "SolidWorks", "MATLAB",
    "Mechanical Design", "Electrical Engineering",
    "Civil Engineering", "Quality Control",
    "Communication", "Problem Solving",
    "Critical Thinking", "Time Management",
    "Customer Service", "Microsoft Office"
]


def clean_resume_text(text):
    if not text:
        return ""

    text = text.replace("\x00", " ")
    text = re.sub(r"[\u200b-\u200f\ufeff]", "", text)

    pattern = r"(?<![a-z])(?:[a-z]\s+){2,}[a-z](?![a-z])"

    text = re.sub(
        pattern,
        lambda m: re.sub(r"\s+", "", m.group()),
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


def extract_skills(resume_text):
    text = clean_resume_text(resume_text).lower()
    found_skills = []

    for skill in sorted(SKILLS_LIST, key=len, reverse=True):
        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-z0-9])"
        )

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


