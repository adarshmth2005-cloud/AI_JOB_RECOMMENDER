
import re

CATEGORY_KEYWORDS = {
    "HR": [
        "human resources", "human resource", "recruitment",
        "talent acquisition", "payroll", "employee relations",
        "hr manager", "hr generalist", "hr coordinator",
        "personnel management"
    ],
    "DESIGNER": [
        "graphic design", "ui design", "ux design",
        "photoshop", "illustrator", "visual design",
        "web designer", "fashion design"
    ],
    "INFORMATION-TECHNOLOGY": [
        "python", "java", "software developer",
        "software engineer", "web developer",
        "data science", "machine learning", "database",
        "networking", "programming", "information technology",
        "javascript", "sql", "computer science"
    ],
    "TEACHER": [
        "teaching", "teacher", "education",
        "lesson planning", "classroom management",
        "curriculum", "academic"
    ],
    "ADVOCATE": [
        "lawyer", "legal", "advocate", "litigation",
        "legal research", "court", "law"
    ],
    "BUSINESS-DEVELOPMENT": [
        "business development", "business strategy",
        "client acquisition", "partnership",
        "business growth"
    ],
    "HEALTHCARE": [
        "healthcare", "nursing", "patient care",
        "clinical", "medical", "hospital"
    ],
    "FITNESS": [
        "fitness", "personal trainer", "gym",
        "physical training", "sports training"
    ],
    "AGRICULTURE": [
        "agriculture", "farming", "agronomy",
        "crop production", "horticulture"
    ],
    "BPO": [
        "bpo", "call center", "customer support",
        "voice process", "non voice process"
    ],
    "SALES": [
        "sales", "sales executive", "sales manager",
        "lead generation", "business sales"
    ],
    "CONSULTANT": [
        "consultant", "consulting", "business consulting",
        "management consulting"
    ],
    "DIGITAL-MEDIA": [
        "digital media", "social media",
        "content creation", "digital marketing",
        "seo", "online marketing"
    ],
    "AUTOMOBILE": [
        "automobile", "automotive", "vehicle",
        "automotive engineering", "auto mechanic"
    ],
    "CHEF": [
        "chef", "cooking", "culinary",
        "food preparation", "kitchen"
    ],
    "FINANCE": [
        "financial analysis", "finance",
        "investment", "financial planning",
        "banking", "financial management"
    ],
    "APPAREL": [
        "apparel", "garment", "textile",
        "fashion merchandising", "clothing"
    ],
    "ENGINEERING": [
        "engineering", "mechanical engineering",
        "electrical engineering", "civil engineering",
        "autocad", "solidworks"
    ],
    "ACCOUNTANT": [
        "accountant", "accounting", "bookkeeping",
        "taxation", "auditing", "accounts payable"
    ],
    "CONSTRUCTION": [
        "construction", "building", "site engineer",
        "civil construction", "project construction"
    ],
    "PUBLIC-RELATIONS": [
        "public relations", "pr manager",
        "media relations", "press release",
        "communications"
    ],
    "BANKING": [
        "banking", "bank manager", "bank operations",
        "loan processing", "credit analysis"
    ],
    "ARTS": [
        "arts", "artist", "painting",
        "music", "performing arts", "creative arts"
    ],
    "AVIATION": [
        "aviation", "pilot", "aircraft",
        "airport", "flight operations"
    ]
}


def predict_resume_category(text):
    if not text:
        return None

    text = re.sub(r"\s+", " ", text.lower())

    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0

        for keyword in keywords:
            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(keyword.lower())
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):
                score += 1

        scores[category] = score

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return None

    return best_category
