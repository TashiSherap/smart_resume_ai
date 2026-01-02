🧠 Smart Resume Analyzer & Builder
AI-Powered ATS Optimization Platform

Analyze resumes. Match job descriptions. Build ATS-friendly resumes — smarter and faster.

🚀 Overview

Smart Resume Analyzer & Builder is a Django-based web application that helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) by analyzing resumes against job descriptions and providing actionable feedback.

✨ Key Features
🔍 Resume Analyzer

Upload resume (PDF / DOCX)

Paste job description

ATS match score (percentage)

Missing keyword detection

Resume improvement suggestions

🛠 Resume Builder

Role-based resume creation

Profile summary support

AI-driven suggestions

Real-time ATS score preview

Resume preview & PDF download

🧩 Tech Stack

Backend: Django (Python)

Frontend: HTML5, Bootstrap 5

Database: SQLite (Django ORM)

AI Logic: Keyword-based ATS scoring + rule-based recommender

PDF Generation: ReportLab

🏗 System Architecture
User Interface (HTML + Bootstrap)
        ↓
Django Views & Controllers
        ↓
AI Engine
(Parser • ATS Scorer • Recommender)
        ↓
SQLite Database
        ↓
PDF Generator

📊 ATS Scoring Logic

Role-based keyword matching

Resume vs Job Description comparison

Missing skills detection

Score capped at 100%

Visual progress bar display

🗃 Database Design

Resume data stored using SQLite

Managed via Django ORM

Accessible through Django Admin Panel

⚙️ Installation & Setup
git clone https://github.com/yourusername/smart-resume-analyzer-builder.git
cd smart-resume-analyzer-builder
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


🔗 Open in browser:
http://127.0.0.1:8000/

🎯 Intended Use

Job seekers improving ATS compatibility

Students learning AI + Django

Final-year / dissertation-level academic project

📌 Future Enhancements

GPT-based resume rewriting

User authentication & accounts

Automatic JD skill extraction

Resume version comparison

Resume ranking system

📄 License

This project is intended for educational and academic use.

⭐ If you find this project helpful, please star the repository!
