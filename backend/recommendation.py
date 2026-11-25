
from skills_extractor import extract_skills


def recommend_jobs(resume_skills, jobs, resume_category=None):
    recommendations = []

    # Resume skills
    resume_skill_list = extract_skills(resume_skills or "")

    resume_skill_set = {
        skill.lower() for skill in resume_skill_list
    }

    for job in jobs:

        # Job required skills
        job_skill_list = extract_skills(job.required_skills or "")

        job_skill_set = {
            skill.lower() for skill in job_skill_list
        }

        # Empty required skills wali jobs skip hongi
        if not job_skill_set:
            continue

        # Matched and missing skills
        matched_skills = resume_skill_set.intersection(job_skill_set)
        missing_skills = job_skill_set - resume_skill_set

        # Calculate skill match percentage
        skill_score = (
            len(matched_skills) / len(job_skill_set)
        ) * 100

        # Divide jobs into three levels
        if skill_score < 40:
            match_level = "Basic"

        elif skill_score < 70:
            match_level = "Intermediate"

        else:
            match_level = "Advanced"

        # Category match
        category_match = (
            bool(resume_category)
            and bool(job.category)
            and resume_category.strip().lower()
            == job.category.strip().lower()
        )

        recommendations.append({
            "job_id": job.id,
            "job_title": job.title,
            "company": job.company,
            "location": job.location,
            "job_category": job.category,
            "category_match": category_match,
            "matched_skills": sorted(list(matched_skills)),
            "missing_skills": sorted(list(missing_skills)),
            "skill_match_percentage": round(skill_score, 2),
            "match_percentage": round(skill_score, 2),
            "match_level": match_level
        })

    # Highest match first
    recommendations.sort(
        key=lambda item: (
            item["skill_match_percentage"],
            item["job_id"]
        ),
        reverse=True
    )

    return recommendations
