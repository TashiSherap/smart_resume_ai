# resume_app/ai_engine/ats_scorer.py

def calculate_ats_score(resume_text, keywords):
    if not resume_text or not keywords:
        return 0

    resume_words = set(resume_text.lower().split())
    matched = 0

    for kw in keywords:
        if kw.lower() in resume_words:
            matched += 1

    score = (matched / len(keywords)) * 100
    return round(score)


print("ats_scorer loaded successfully")
