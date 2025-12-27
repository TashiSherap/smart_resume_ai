# ai_engine/recommender.py

from .constants import ROLE_KEYWORDS


def generate_recommendations(skills="", education="", experience="", role="backend"):
    """
    Generates ATS score and AI suggestions.
    Role-aware, UI-compatible, string-safe.
    """

    ats_score = 0

    # --------------------------
    # Skills
    # --------------------------
    if isinstance(skills, str) and skills.strip():
        skills_list = [s.strip().lower() for s in skills.split(",")]
        ats_score += len(skills_list) * 10
        skills_suggestion = "Good skill coverage. Consider adding role-specific tools."
    else:
        skills_list = []
        skills_suggestion = "Add relevant technical and soft skills."

    # --------------------------
    # Education
    # --------------------------
    if isinstance(education, str) and education.strip():
        ats_score += 20
        education_suggestion = "Education section looks good."
    else:
        education_suggestion = "Include degree, institution, and graduation year."

    # --------------------------
    # Experience
    # --------------------------
    if isinstance(experience, str) and experience.strip():
        ats_score += 30
        experience_suggestion = "Good experience. Quantify impact using numbers."
    else:
        experience_suggestion = "Add measurable achievements and action verbs."

    ats_score = min(ats_score, 100)

    # --------------------------
    # Role-based missing keywords
    # --------------------------
    role_keywords = ROLE_KEYWORDS.get(role, ROLE_KEYWORDS["backend"])
    missing_keywords = [kw for kw in role_keywords if kw.lower() not in skills_list]

    if missing_keywords:
        skills_suggestion += f" Missing role keywords: {', '.join(missing_keywords)}"

    return {
        "ats_score": ats_score,
        "skills": skills_suggestion,
        "education": education_suggestion,
        "experience": experience_suggestion,
    }
