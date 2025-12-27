def calculate_jd_match(resume_text, job_description):
    if not resume_text or not job_description:
        return 0

    resume_words = set(resume_text.lower().split())
    jd_words = set(job_description.lower().split())

    if not resume_words:
        return 0

    match_count = len(resume_words.intersection(jd_words))
    score = (match_count / len(resume_words)) * 100

    return round(score, 2)

print("jd_matcher loaded successfully")
