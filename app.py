from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import io
from datetime import datetime
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from resume_utils import (
    extract_text,
    clean_text,
    extract_skills,
    predict_role,
    calculate_ats,
    extract_projects,
    extract_certifications,
    extract_contact_info,
    missing_skills
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 # 10MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_quality_level(ats_score):
    """ATS score quality + readiness level"""
    if ats_score >= 90:
        return "Expert", "Professional"
    elif ats_score >= 75:
        return "Advanced", "Professional"
    elif ats_score >= 60:
        return "Intermediate", "Advanced"
    elif ats_score >= 40:
        return "Beginner", "Intermediate"
    else:
        return "Beginner", "Beginner"


def categorize_skills(skills):
    """Skills are divided into proper categories"""
    categories = {
        "Web Development": [],
        "Frameworks & Libraries": [],
        "Programming Languages": [],
        "Databases": [],
        "Cloud & DevOps": [],
        "Data Science & ML": [],
        "Tools & Others": []
    }

    skill_map = {
        "Web Development": ["html", "html5", "css", "css3", "sass", "scss", "bootstrap", "tailwind", "material ui", "responsive design", "dom", "ajax", "rest api", "graphql","javascript"],
        "Frameworks & Libraries": ["react", "react.js", "angular", "vue", "vue.js", "next.js", "nuxt", "svelte", "django", "flask", "fastapi", "nodejs", "node.js", "express", "spring", "laravel", "jquery", "redux"],
        "Programming Languages": ["python", "java", "c++", "c#","typescript", "ts", "go", "golang", "rust", "kotlin", "swift", "c", "r", "php", "ruby", "scala"],
        "Databases": ["sql", "mysql", "postgresql", "postgres", "mongodb", "mongo", "redis", "dbms", "sqlite", "oracle", "cassandra", "firebase"],
        "Cloud & DevOps": ["aws", "azure", "gcp", "docker", "kubernetes", "k8s", "terraform", "lambda", "s3", "ec2", "jenkins", "github actions", "ci/cd", "devops"],
        "Data Science & ML": ["pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "sklearn", "tableau", "powerbi", "excel", "statistics", "eda", "machine learning", "ml", "deep learning", "tensorflow", "pytorch", "keras", "nlp", "computer vision", "llm", "langchain"],
        "Tools & Others": ["git", "github", "gitlab", "linux", "bash", "vs code", "vscode", "jupyter", "postman", "figma", "jira"]
    }

    for skill in skills:
        skill_lower = skill.lower().strip()
        categorized = False

        # Priority: Web Dev > Frameworks > Programming
        for cat, cat_skills in skill_map.items():
            if any(s == skill_lower or s in skill_lower.split() for s in cat_skills):
                if skill not in categories[cat]:
                    categories[cat].append(skill)
                categorized = True
                break

        if not categorized:
            if skill not in categories["Tools & Others"]:
                categories["Tools & Others"].append(skill)

    return {k: v for k, v in categories.items() if v}

def generate_pdf_report(data):
    """ReportLab tho professional PDF report"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        spaceAfter=30,
        alignment=1
    )

    story.append(Paragraph("AI Resume Intelligence Report", title_style))
    story.append(Spacer(1, 12))

    # Candidate Info Table
    story.append(Paragraph("Candidate Information", styles['Heading2']))
    candidate_data = [
        ["Name", data['contact']['name']],
        ["Email", data['contact']['email']],
        ["Phone", data['contact']['phone']],
        ["GitHub", data['contact']['github']],
        ["LinkedIn", data['contact']['linkedin']],
        ["Predicted Role", data['predicted_role']],
        ["ATS Score", f"{data['ats_score']}/100 - {data['ats_level']}"],
        ["Quality Level", data['quality_level']],
        ["Market Readiness", data['readiness']]
    ]
    t = Table(candidate_data, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Skills
    story.append(Paragraph(f"Skills Found ({len(data['skills_found'])})", styles['Heading2']))
    skills_text = ", ".join(data['skills_found'][:30])
    story.append(Paragraph(skills_text, styles['Normal']))
    story.append(Spacer(1, 20))

    # Missing Skills
    if data['missing_skills']:
        story.append(Paragraph("Missing Skills / Recommendations", styles['Heading2']))
        missing_text = ", ".join(data['missing_skills'])
        story.append(Paragraph(missing_text, styles['Normal']))
        story.append(Spacer(1, 20))

    # Feedback
    story.append(Paragraph("Recruiter Feedback", styles['Heading2']))
    story.append(Paragraph(data['feedback'], styles['Normal']))
    story.append(Spacer(1, 20))

    # Roadmap
    story.append(Paragraph("Recommended Career Path", styles['Heading2']))
    for i, step in enumerate(data['roadmap'], 1):
        story.append(Paragraph(f"{i}. {step}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """AJAX API for dashboard - returns JSON"""
    if 'resume' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Use PDF, DOCX or TXT"}), 400

    try:
        filename = secure_filename(file.filename)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        # Extract text
        text = extract_text(file, filename)

        if not text or len(text.strip()) < 50:
            return jsonify({"error": "Resume text too short or unreadable"}), 400

        words, text_lower = clean_text(text)
        contact = extract_contact_info(text)
        skills = extract_skills(words)

        # Deduplicate skills
        skills = list(set([s.strip() for s in skills if s.strip()]))

        predicted_role = predict_role(skills)
        ats_score = calculate_ats(text, skills)
        quality_level, readiness = get_quality_level(ats_score)

        # ATS level text
        if ats_score >= 90:
            ats_level = "Excellent"
        elif ats_score >= 75:
            ats_level = "Strong"
        elif ats_score >= 60:
            ats_level = "Moderate"
        else:
            ats_level = "Needs Improvement"

        projects = extract_projects(text)
        certifications = extract_certifications(text)
        missing = missing_skills(skills, predicted_role)
        skill_categories = categorize_skills(skills)

        # Feedback
        if ats_score >= 85:
            feedback = "Excellent resume! Strong ATS compatibility and relevant skills. Ready for top companies."
        elif ats_score >= 70:
            feedback = "Good resume with solid foundation. Minor improvements recommended for better ATS scores."
        elif ats_score >= 50:
            feedback = "Decent resume but needs optimization. Add more keywords and quantify achievements."
        else:
            feedback = "Resume needs significant improvements. Focus on skills, projects, and formatting."

        # Roadmap
        roadmap = {
            "Backend Developer": ["Master Python & OOP", "Learn Flask/Django Frameworks", "Master SQL & Databases", "Build REST APIs & Deploy"],
            "Frontend Developer": ["Master HTML5 & CSS3", "Learn JavaScript ES6+", "Learn React/Next.js", "Build Responsive Projects"],
            "Data Scientist": ["Master Python for Data", "Learn Pandas & NumPy", "Machine Learning Algorithms", "Deep Learning & Model Deployment"],
            "DevOps Engineer": ["Master Linux & Bash", "Learn Docker & Kubernetes", "Master AWS/Cloud Platforms", "CI/CD & Infrastructure"],
            "AI/ML Engineer": ["Master Python & Math", "Deep Learning & PyTorch", "LLM & Generative AI", "MLOps & Deployment"],
            "Software Engineer": ["Master DSA & OOP", "Learn System Design", "Master Version Control", "Build Full Stack Projects"],
            "Cloud Engineer": ["Master AWS/Azure/GCP", "Learn Docker & K8s", "Terraform & IaC", "CI/CD Pipelines"],
            "Fresher": ["Learn Programming Fundamentals", "Build 3-4 Projects", "Master Git & GitHub", "Practice DSA Daily"]
        }

        career_path = roadmap.get(predicted_role, roadmap["Fresher"])

        result = {
            "contact": contact,
            "skills_found": skills,
            "skills_count": len(skills),
            "predicted_role": predicted_role,
            "ats_score": ats_score,
            "ats_level": ats_level,
            "quality_level": quality_level,
            "readiness": readiness,
            "projects": projects,
            "projects_count": 1 if "No Projects" not in projects else 0,
            "certifications": certifications,
            "certifications_count": len(certifications.split('\n')) if "No Certifications" not in certifications else 0,
            "missing_skills": missing,
            "missing_count": len(missing) if missing and "✨" not in missing[0] else 0,
            "skill_categories": skill_categories,
            "feedback": feedback,
            "roadmap": career_path,
            "file_name": filename,
            "file_size": f"{file_size / 1024:.1f} KB",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "raw_text": text
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Error processing resume: {str(e)}"}), 500

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    """PDF Report Download"""
    data = request.json
    pdf_buffer = generate_pdf_report(data)
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"AI_Resume_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

@app.route('/export/json', methods=['POST'])
def export_json():
    """JSON Data Export"""
    data = request.json
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    buffer = io.BytesIO(json_str.encode('utf-8'))
    return send_file(
        buffer,
        mimetype='application/json',
        as_attachment=True,
        download_name=f"resume_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)