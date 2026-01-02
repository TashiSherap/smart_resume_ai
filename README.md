🧠 Smart Resume Analyzer & Builder

An AI-powered web application that analyzes resumes against job descriptions, calculates ATS match scores, highlights missing keywords, and helps users build ATS-optimized resumes with smart suggestions.

🚀 Features
🔍 Resume Analyzer

Upload resume (PDF/DOCX)

Paste job description

ATS match score (%)

Missing keyword detection

Improvement suggestions

🛠 Resume Builder

Role-based resume creation

Profile summary support

AI suggestions for skills, education & experience

ATS score preview

Resume preview & PDF download

🧩 Tech Stack

Backend: Django (Python)

Frontend: HTML, Bootstrap 5

Database: SQLite

AI Logic: Keyword-based ATS + rule-based recommendations

PDF Generation: ReportLab

🏗 Architecture Overview
Frontend (HTML + Bootstrap)
        |
Django Views
        |
AI Engine (Parser • ATS Scorer • Recommender)
        |
SQLite Database
        |
PDF Generator

📊 ATS Scoring

Role-specific keyword matching

Job Description vs Resume comparison

Missing skills identification

ATS score shown as percentage

🗃 Database

Resume data stored in SQLite

Managed via Django ORM

Accessible through Django Admin Panel

⚙️ Setup
git clone https://github.com/yourusername/smart-resume-analyzer-builder.git
cd smart-resume-analyzer-builder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


Visit:
👉 http://127.0.0.1:8000/

🎯 Use Case

Job seekers optimizing resumes for ATS

Students learning AI + Django integration

Academic final year / dissertation project

📌 Future Enhancements

GPT-based resume rewriting

User authentication

JD skill auto-extraction

Resume version comparison

📄 License

Educational use only.

⭐ If you find this project useful, consider starring the repository!
