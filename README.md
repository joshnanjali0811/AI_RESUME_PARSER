<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/3135/3135765.png" alt="Resume Parser AI" width="120"/>
</p>

<h1 align="center">📄 Resume Parser AI</h1>
<h3 align="center">AI-Powered Resume Analysis & ATS Optimization System</h3>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Flask-3.0-000?style=for-the-badge&logo=flask&logoColor=white"/></a>
  <a href="#"><img src="https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge&logo=spacy&logoColor=white"/></a>
  <a href="#"><img src="https://img.shields.io/badge/NLTK-Text%20Processing-56B3FA?style=for-the-badge&logo=nltk&logoColor=white"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/></a>
</p>

<p align="center">
  <b>Extract Skills • Predict Role • ATS Score • Career Roadmap • 100% Local Processing</b>
</p>

<p align="center">
  <img src="https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=800&h=400&fit=crop" alt="AI Robot Analyzing Resume" width="800"/>
  <br><i>AI Resume Parser - 100% Privacy, No External APIs</i>
</p>

---

### 🎯 Project Overview

**Problem Statement:**  
Recruiters face difficulty manually screening hundreds of resumes for a single job. Reviewing them is time-consuming and inefficient. Many candidates also include unnecessary keywords, making selection less accurate.

**Objective:**  
Develop an AI-based Resume Parser that can:
- Automatically analyze uploaded resumes  
- Extract important technical skills  
- Predict suitable job roles  
- Calculate ATS (Applicant Tracking System) score  
- Provide recruiter feedback + career roadmap suggestions  

---

### ✨ Key Features

| Feature | Details |
| --- | --- |
| **📤 Resume Upload** | PDF, DOCX, TXT support with validation |
| **🧠 Skill Extraction** | 100+ tech skills from 7 job categories using regex + NER |
| **📊 ATS Score** | 7-point breakdown: Sections, Skills, Impact, Formatting |
| **🎯 Role Prediction** | Software Eng, AI/ML, Backend, Frontend, DevOps, Cloud, Data Science |
| **🔍 Missing Skills** | Role-specific gap analysis with top 6 suggestions |
| **💬 Recruiter Feedback** | Dynamic feedback based on score tiers |
| **🗺️ Career Roadmap** | 4-step learning path for predicted role |
| **📄 Raw Sections** | Extracts Projects & Certifications as raw text |
| **⚠️ Scan Detection** | Warns for image-based PDFs with <50 chars |
| **🎨 Modern UI** | Glassmorphism dashboard + animated charts + responsive |
| **🔄 Try Another Resume** | Reset and analyze new resume without refresh |
| **🔒 Privacy First** | All parsing local. No external APIs |

---

### 📊 ATS Scoring - 100 Points

| Component | Points | Checks |
| --- | --- | --- |
| **Resume Sections** | 20 | Education, Experience, Projects, Skills, Certifications |
| **Skills Breadth** | 25 | Extracted skills vs skill database ratio |
| **Impact Metrics** | 15 | %, increased, improved, optimized, scaled keywords |
| **Projects Section** | 15 | Bonus if Projects section found |
| **Certifications** | 10 | Bonus if Certifications section found |
| **Formatting** | 10 | Bullet points • or - usage |
| **Role Keywords** | 5 | software, developer, engineer mentions |

**Score Tiers**: 🏆 80+ Excellent | ✨ 60-79 Great | 👍 40-59 Good | ⚠️ <40 Needs Work

---

### 🛠️ Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,html,css,javascript"/>
</p>

**Backend**: Flask 3.0.3  
**PDF/DOCX**: PyPDF2 3.0.1, python-docx 1.1.0  
**NLP**: NLTK 3.8.1 for stopwords, spaCy 3.7.5 for NER  
**Charts**: Chart.js for analytics  
**Frontend**: HTML5, CSS3, JavaScript, Inter Font, Glassmorphism UI

---

### 🧠 Model / Algorithm

**Approach:** Rule-Based NLP instead of Deep Learning  
**Why:** Simple, efficient for small datasets, fast processing, no training data needed

**Techniques Used:**  
- **NLP**: Text cleaning, tokenization, stopwords removal, skill identification  
- **Keyword Matching**: Compare resume text with 100+ skill database  
- **Rule-Based Classification**: 
    - `Python + Flask` → Backend Developer  
    - `ML + Pandas` → Data Scientist  
    - `HTML + CSS + React` → Frontend Developer  
    - `AWS + Docker` → DevOps Engineer

**Output:** Extracted Skills, Predicted Role, ATS Score, Missing Skills, Feedback, Roadmap

---

### 📊 Project Workflow

1. **Resume Upload** → User uploads PDF/DOCX/TXT via sidebar
2. **Text Extraction** → PyPDF2/python-docx extracts raw text
3. **Preprocessing** → Lowercase + regex cleaning + NLTK stopwords removal
4. **Skill Extraction** → Match cleaned text with skill database
5. **Role Prediction** → Rule-based classification on extracted skills
6. **ATS Score Calculation** → 7-component scoring system
7. **Result Generation** → Dashboard with skills, role, score, charts, feedback, roadmap

---

### 🎯 Supported Roles

1. **Software Engineer** - Java, Spring Boot, Microservices, Docker, System Design
2. **AI/ML Engineer** - Python, PyTorch, TensorFlow, LLMs, LangChain, RAG, Vector DB
3. **Backend Developer** - Django, Flask, FastAPI, PostgreSQL, Redis, API Design
4. **Frontend Developer** - React, Next.js, TypeScript, Tailwind, Redux
5. **Data Scientist** - Pandas, NumPy, Scikit-learn, Spark, Tableau, Airflow
6. **DevOps Engineer** - Docker, Kubernetes, AWS, Terraform, CI/CD, Jenkins
7. **Cloud Engineer** - AWS, Azure, GCP, CloudFormation, VPC, Lambda

---

### 🚀 Quick Start

```bash

# 1. Clone the repository from GitHub
git clone https://github.com/joshnanjali0811/AI_RESUME_PARSER.git
cd AI_RESUME_PARSER

# 2. Create virtual environment to isolate dependencies
# Windows command
python -m venv
venv\Scripts\activate

# Mac/Linux command  
# python3 -m venv
# source venv/bin/activate

# 3. Install all required packages
pip install -r requirements.txt

# 4. Run the Flask application
python app.py

# 5. Open the app in your browser
# Go to: http://localhost:5000

```
### 📂 Project Structure

```bash
Resume-Parser-AI/
├── app.py                      # Flask routes + ATS logic + PDF/JSON export
├── resume_utils.py             # Text extraction + skill extraction engine
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Jinja2 dashboard template
├── static/
│   ├── style.css               # Glassmorphism CSS + responsive design
│   └── script.js               # AJAX + Chart.js + dashboard logic
└── README.md                   # Documentation
```
### 📌requirements.txt

```bash
Flask==3.0.3
PyPDF2==3.0.1
python-docx==1.1.0
nltk==3.8.1
spacy==3.7.5
reportlab==4.0.7
werkzeug==3.0.1
```
### 👨‍💻 Author

Let Your Resume Meet Its Destiny ✨

Crafted by Joshnanjali ❤️  |  © 2026 AI Resume Parser 