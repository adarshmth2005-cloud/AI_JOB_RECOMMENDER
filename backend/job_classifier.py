
CATEGORY_KEYWORDS = {
    "HR": [
        "human resources", "recruitment", "recruiter",
        "talent acquisition", "payroll", "employee relations"
    ],
    "DESIGNER": [
        "graphic designer", "ui designer", "ux designer",
        "fashion designer", "web designer"
    ],
    "INFORMATION-TECHNOLOGY": [
        "python developer", "python programmer",
        "java developer", "software developer",
        "software engineer", "web developer",
        "frontend developer", "backend developer",
        "full stack developer", "programmer",
        "data scientist", "machine learning",
        "IT support", "network engineer",
        "database administrator", "cybersecurity",
        "system administrator", "data analyst",
        "devops engineer", "cloud engineer"
    ],
    "TEACHER": [
        "teacher", "professor", "lecturer", "instructor",
        "academic", "education"
    ],
    "ADVOCATE": [
        "lawyer", "advocate", "legal advisor",
        "attorney", "legal counsel"
    ],
    "BUSINESS-DEVELOPMENT": [
        "business development", "business analyst",
        "business manager"
    ],
    "HEALTHCARE": [
        "doctor", "nurse", "medical", "healthcare",
        "clinical", "pharmacist"
    ],
    "FITNESS": [
        "fitness trainer", "personal trainer",
        "gym instructor", "sports coach"
    ],
    "AGRICULTURE": [
        "agriculture", "agronomist", "farm manager",
        "agricultural engineer"
    ],
    "BPO": [
        "call center", "customer support",
        "customer service representative", "bpo"
    ],
    "SALES": [
        "sales executive", "sales manager",
        "sales representative", "sales associate"
    ],
    "CONSULTANT": [
        "consultant", "consulting", "business consultant"
    ],
    "DIGITAL-MEDIA": [
        "digital marketing", "social media",
        "content creator", "seo", "media"
    ],
    "AUTOMOBILE": [
        "automotive", "automobile", "mechanic",
        "vehicle technician"
    ],
    "CHEF": [
        "chef", "cook", "kitchen manager",
        "culinary"
    ],
    "FINANCE": [
        "financial analyst", "financial controller",
        "investment analyst", "finance manager",
        "financial advisor"
    ],
    "APPAREL": [
        "apparel", "garment", "textile",
        "fashion merchandiser"
    ],
    "ENGINEERING": [
        "mechanical engineer", "civil engineer",
        "electrical engineer", "engineering"
    ],
    "ACCOUNTANT": [
        "accountant", "accounting", "bookkeeper",
        "auditor", "tax accountant"
    ],
    "CONSTRUCTION": [
        "construction manager", "site engineer",
        "building contractor"
    ],
    "PUBLIC-RELATIONS": [
        "public relations", "pr manager",
        "communications manager"
    ],
    "BANKING": [
        "banker", "banking", "loan officer",
        "credit analyst"
    ],
    "ARTS": [
        "artist", "photographer", "illustrator",
        "musician", "actor"
    ],
    "AVIATION": [
        "pilot", "aviation", "flight attendant",
        "aircraft technician"
    ]
}


def classify_job(title, description=""):
    text = (
        (title or "") + " " + (description or "")
    ).lower()

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(
            1 for keyword in keywords
            if keyword in text
        )

        if score > 0:
            scores[category] = score

    if not scores:
        return None

    return max(scores, key=scores.get)

