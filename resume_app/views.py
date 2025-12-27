import re
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Resume
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from .ai_engine.resume_parser import parse_resume
from .ai_engine.ats_scorer import calculate_ats_score
from .ai_engine.recommender import generate_recommendations
from .ai_engine.constants import ROLE_KEYWORDS


def extract_keywords(text):
    """
    Simple keyword extraction from text:
    - Lowercase
    - Split on non-word characters
    - Remove stopwords
    """
    stopwords = set(["and", "or", "the", "a", "an", "with", "to", "for", "in", "on", "of", "at"])
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = list(set([w for w in words if w not in stopwords]))
    return keywords


# -------------------------------
# HOME (Analyzer only)
# -------------------------------
def home(request):
    ats_score = None
    missing_keywords = []
    suggestions = []
    section_scores = None
    selected_role = "backend"
    job_description = ""

    if request.method == "POST" and "resume" in request.FILES:
        # -------- FORM DATA --------
        resume_file_obj = request.FILES["resume"]
        job_description = request.POST.get("job_description", "").strip()
        selected_role = request.POST.get("role", "backend")

        # -------- PARSE RESUME --------
        resume_text = parse_resume(resume_file_obj).lower()
        jd_text = job_description.lower()

        # -------- ROLE KEYWORDS --------
        role_keywords = ROLE_KEYWORDS.get(selected_role, ROLE_KEYWORDS["backend"])

        # -------- ATS SCORE --------
        combined_text = resume_text + " " + jd_text
        ats_score = calculate_ats_score(combined_text, role_keywords)

        # -------- MISSING KEYWORDS --------
        missing_keywords = [kw for kw in role_keywords if kw not in combined_text]

        # -------- BASIC SECTION FEEDBACK --------
        section_scores = {
            "skills": min(100, ats_score + 5),
            "experience": ats_score,
            "education": max(40, ats_score - 10),
        }

        # -------- AI SUGGESTIONS --------
        if missing_keywords:
            suggestions.append(
                "Consider adding missing role-specific keywords to improve ATS match."
            )
        if ats_score < 60:
            suggestions.append(
                "Your resume needs better alignment with the job description."
            )
        if ats_score >= 80:
            suggestions.append(
                "Your resume is well-optimized for this role."
            )

    return render(
        request,
        "resume_app/home.html",
        {
            "ats_score": ats_score,
            "missing_keywords": missing_keywords,
            "section_scores": section_scores,
            "suggestions": suggestions,
            "selected_role": selected_role,
            "job_description": job_description,
        },
    )


# -------------------------------
# RESUME BUILDER
# -------------------------------
def resume_builder(request):
    resume = None
    suggestions = {}
    ats_score = None
    selected_role = "backend"

    # Load existing resume if editing
    resume_id = request.GET.get("resume_id")
    if resume_id:
        resume = get_object_or_404(Resume, id=resume_id)
        selected_role = resume.role

    if request.method == "POST":
        # ---- FORM DATA ----
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        profile = request.POST.get("profile", "").strip()
        profile_summary = request.POST.get("profile_summary", "").strip()
        skills = request.POST.get("skills", "").strip()
        education = request.POST.get("education", "").strip()
        experience = request.POST.get("experience", "").strip()
        selected_role = request.POST.get("role", "backend")

        # ---- ATS SCORING ----
        ats_keywords = ROLE_KEYWORDS.get(
            selected_role,
            ROLE_KEYWORDS["backend"]
        )

        combined_text = " ".join([
            profile_summary,
            skills,
            education,
            experience
        ])

        ats_score = calculate_ats_score(combined_text, ats_keywords)

        # ---- AI SUGGESTIONS ----
        ai_output = generate_recommendations(
            skills,
            education,
            experience,
            selected_role
        )

        suggestions = {
            "skills": ai_output.get("skills", ""),
            "education": ai_output.get("education", ""),
            "experience": ai_output.get("experience", ""),
        }

        # ---- SAVE / UPDATE ----
        if resume:
            resume.full_name = name
            resume.email = email
            resume.phone = phone
            resume.profile = profile
            resume.profile_summary = profile_summary
            resume.skills = skills
            resume.education = education
            resume.experience = experience
            resume.role = selected_role
            resume.save()
        else:
            resume = Resume.objects.create(
                full_name=name,
                email=email,
                phone=phone,
                profile=profile,
                profile_summary=profile_summary,
                skills=skills,
                education=education,
                experience=experience,
                role=selected_role,
            )

        # ---- PREVIEW PAGE ----
        return render(
            request,
            "resume_app/preview_resume.html",
            {
                "resume": resume,
                "ats_score": ats_score,
                "selected_role": selected_role,
                "suggestions": suggestions,
            }
        )

    # ---- BUILDER PAGE ----
    return render(
        request,
        "resume_app/resume_builder.html",
        {
            "resume": resume,
            "suggestions": suggestions,
            "selected_role": selected_role,
        }
    )


# -------------------------------
# PREVIEW RESUME (CONSISTENT ATS)
# -------------------------------
def preview_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    ats_keywords = ROLE_KEYWORDS.get(
        resume.role,
        ROLE_KEYWORDS["backend"]
    )

    combined_text = (
        f"{resume.profile_summary} "
        f"{resume.skills} {resume.education} {resume.experience}"
    )

    ats_score = calculate_ats_score(combined_text, ats_keywords)

    ai_output = generate_recommendations(
        resume.skills,
        resume.education,
        resume.experience,
        resume.role,
    )

    suggestions = {
        "skills": ai_output.get("skills"),
        "education": ai_output.get("education"),
        "experience": ai_output.get("experience"),
    }

    return render(
        request,
        "resume_app/preview_resume.html",
        {
            "resume": resume,
            "ats_score": ats_score,
            "selected_role": resume.role,
            "suggestions": suggestions,
        },
    )




# -------------------------------
# PDF GENERATION
# -------------------------------
def generate_pdf(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{resume.full_name}_resume.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 50

    # ---------------- HEADER ----------------
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2, y, resume.full_name)
    y -= 25

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(
        width / 2,
        y,
        f"{resume.email} | {resume.phone}"
    )
    y -= 18

    if resume.profile:
        pdf.setFont("Helvetica-Oblique", 11)
        pdf.drawCentredString(width / 2, y, resume.profile)
        y -= 18

    pdf.setFont("Helvetica-Oblique", 11)
    pdf.drawCentredString(
        width / 2,
        y,
        f"Target Role: {resume.role.replace('_', ' ').title()}"
    )
    y -= 40

    # ---------------- SECTIONS ----------------
    sections = [
        ("Profile Summary", resume.profile_summary),
        ("Skills", resume.skills),
        ("Education", resume.education),
        ("Experience", resume.experience),
    ]

    for title, content in sections:
        if not content:
            continue

        # Page break safety
        if y < 120:
            pdf.showPage()
            y = height - 50

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, title)
        y -= 20

        pdf.setFont("Helvetica", 12)
        text = pdf.beginText(50, y)
        text.textLines(content)
        pdf.drawText(text)

        y -= 80

    pdf.showPage()
    pdf.save()
    return response


