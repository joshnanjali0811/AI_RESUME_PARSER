let currentData = null;
const fileInput = document.getElementById('fileInput');
const uploadZone = document.getElementById('uploadZone');
const filePreview = document.getElementById('filePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const exportPDF = document.getElementById('exportPDF');
const exportJSON = document.getElementById('exportJSON');
const tryAgainBtn = document.getElementById('tryAgainBtn');

// Sidebar navigation
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        if (!currentData) return;

        document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
        item.classList.add('active');

        const section = item.dataset.section;
        document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
        document.getElementById(section + '-section').classList.add('active');
        document.getElementById('pageTitle').textContent = item.querySelector('span:last-child').textContent;
    });
});

// File upload handling
fileInput.addEventListener('change', handleFileSelect);
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--primary)';
    uploadZone.style.background = 'rgba(99, 102, 241, 0.1)';
});
uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.borderColor = 'var(--border)';
    uploadZone.style.background = 'var(--bg-tertiary)';
});
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--border)';
    uploadZone.style.background = 'var(--bg-tertiary)';
    handleFileSelect({ target: { files: e.dataTransfer.files } });
});

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!file) return;

    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = (file.size / 1024 / 1024).toFixed(2) + ' MB';
    filePreview.classList.remove('hidden');
    uploadZone.style.display = 'none';
}

analyzeBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('resume', file);

    loadingOverlay.classList.remove('hidden');
    simulateProgress();

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            alert(data.error);
            loadingOverlay.classList.add('hidden');
            return;
        }

        currentData = data;
        displayResults(data);
        loadingOverlay.classList.add('hidden');

    } catch (err) {
        alert('Error analyzing resume: ' + err.message);
        loadingOverlay.classList.add('hidden');
    }
});

function simulateProgress() {
    const steps = [
        'Extracting Skills...',
        'Predicting Role...',
        'Calculating ATS Score...',
        'Generating Insights...'
    ];
    let step = 0;
    const progressFill = document.getElementById('progressFill');
    const loadingStep = document.getElementById('loadingStep');

    const interval = setInterval(() => {
        progressFill.style.width = ((step + 1) * 25) + '%';
        if (step < steps.length) {
            loadingStep.textContent = steps[step];
        }
        step++;
        if (step >= 4) clearInterval(interval);
    }, 800);
}

function displayResults(data) {
    document.getElementById('welcome-section').classList.remove('active');
    document.getElementById('dashboard-section').classList.add('active');

    exportPDF.style.display = 'block';
    exportJSON.style.display = 'block';
    tryAgainBtn.style.display = 'block';

    // CANDIDATE DETAILS
    document.getElementById('candName').textContent = data.contact.name || 'Not found';
    document.getElementById('candEmail').textContent = data.contact.email || 'Not found';
    document.getElementById('candPhone').textContent = data.contact.phone || 'Not found';
    document.getElementById('candGithub').textContent = data.contact.github || 'Not found';
    document.getElementById('candLinkedin').textContent = data.contact.linkedin || 'Not found';

    // ATS circular progress - radius 60 = circumference 377
    const circle = document.getElementById('progressCircle');
    const circumference = 377;
    const offset = circumference - (circumference * data.ats_score / 100);
    circle.style.strokeDashoffset = offset;
    document.getElementById('atsScoreValue').textContent = data.ats_score;
    document.getElementById('atsLevel').textContent = data.ats_level;

    // Role
    document.getElementById('predictedRole').textContent = data.predicted_role;
    document.getElementById('qualityLevel').textContent = 'Quality: ' + data.quality_level;
    document.getElementById('readiness').textContent = 'Market Readiness: ' + data.readiness;

    // Feedback
    document.getElementById('feedbackText').textContent = data.feedback;

    // Skills
    const skillsContainer = document.getElementById('skillsContainer');
    skillsContainer.innerHTML = data.skills_found.map(s => `<span class="badge">${s}</span>`).join('');

    // Missing skills
    const missingContainer = document.getElementById('missingContainer');
    if (data.missing_skills.length > 0 &&!data.missing_skills[0].includes('✨')) {
        missingContainer.innerHTML = data.missing_skills.map(s => `• ${s}`).join('<br>');
    } else {
        missingContainer.innerHTML = data.missing_skills[0] || 'No missing skills found! Your resume is well optimized.';
    }

    // Categories - Skills Section boxes
    const categoriesGrid = document.getElementById('categoriesGrid');
    categoriesGrid.innerHTML = Object.entries(data.skill_categories).map(([cat, skills]) => `
        <div class="card">
            <h4>${cat} (${skills.length})</h4>
            <p style="color: var(--text-muted); margin-top: 10px; font-size: 13px;">${skills.join(', ')}</p>
        </div>
    `).join('');

    // Projects & certs
    document.getElementById('projectsRaw').textContent = data.projects;
    document.getElementById('certsRaw').textContent = data.certifications;

    // REPORTS SECTION - Fallback if no text extracted
    const rawResumeEl = document.getElementById('rawResume');
    if (data.raw_text && data.raw_text.trim().length > 50) {
        rawResumeEl.textContent = data.raw_text;
    } else {
        rawResumeEl.innerHTML = `
            <div class="empty-resume-msg">
                <div class="empty-icon">📄</div>
                <h3>No text extracted</h3>
                <p>
                    Could not extract text from your resume.<br><br>
                    <strong>Solutions:</strong><br>
                    1. Use text-based PDF/DOCX files<br>
                    2. If scanned PDF, convert using OCR tool<br>
                    3. Copy-paste content and save as TXT file<br><br>
                    💡 Tip: "Save As PDF" from MS Word gives best results
                </p>
            </div>
        `;
    }

    // Roadmap
    const roadmapList = document.getElementById('roadmapList');
    roadmapList.innerHTML = data.roadmap.map(step => `<li>${step}</li>`).join('');

    renderCharts(data);
}

function renderCharts(data) {
    if (window.doughnutChart && typeof window.doughnutChart.destroy === 'function') {
        window.doughnutChart.destroy();
    }
    if (window.barChart && typeof window.barChart.destroy === 'function') {
        window.barChart.destroy();
    }

    const ctx1 = document.getElementById('doughnutChart');
    if (ctx1) {
        window.doughnutChart = new Chart(ctx1.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Skills Found', 'Missing Skills'],
                datasets: [{
                    data: [data.skills_count, data.missing_count],
                    backgroundColor: ['#6366f1', '#ef4444'],
                    borderWidth: 2,
                    borderColor: '#0b1120'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#cbd5e1', font: { size: 12 } }
                    }
                }
            }
        });
    }

    const ctx2 = document.getElementById('barChart');
    if (ctx2) {
        const categories = Object.keys(data.skill_categories);
        const counts = Object.values(data.skill_categories).map(arr => arr.length);
        window.barChart = new Chart(ctx2.getContext('2d'), {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Skills per Category',
                    data: counts,
                    backgroundColor: '#8b5cf6',
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: {
                        ticks: { color: '#94a3b8', font: { size: 11 } },
                        grid: { color: 'rgba(148, 163, 184, 0.1)' }
                    },
                    x: {
                        ticks: { color: '#94a3b8', font: { size: 10 } },
                        grid: { display: false }
                    }
                }
            }
        });
    }
}

function toggleRaw(id) {
    const el = document.getElementById(id);
    el.style.display = el.style.display === 'none'? 'block' : 'none';
}

function searchResume() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const content = document.getElementById('rawResume');
    const originalText = currentData? currentData.raw_text : '';

    if (search && originalText && originalText.trim().length > 50) {
        const regex = new RegExp(search, 'gi');
        const highlighted = originalText.replace(regex, match => `<mark style="background: #fbbf24; color: #000; padding: 2px;">${match}</mark>`);
        content.innerHTML = highlighted;
    } else {
        content.textContent = originalText;
    }
}

// Export handlers
exportPDF.addEventListener('click', async () => {
    if (!currentData) return;
    const response = await fetch('/export/pdf', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(currentData)
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'AI_Resume_Report.pdf';
    a.click();
});

exportJSON.addEventListener('click', async () => {
    if (!currentData) return;
    const response = await fetch('/export/json', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(currentData)
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'resume_data.json';
    a.click();
});

// Try Another Resume - Reset function
tryAgainBtn.addEventListener('click', resetDashboard);

function resetDashboard() {
    currentData = null;
    fileInput.value = '';

    document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
    document.getElementById('welcome-section').classList.add('active');

    exportPDF.style.display = 'none';
    exportJSON.style.display = 'none';
    tryAgainBtn.style.display = 'none';

    filePreview.classList.add('hidden');
    uploadZone.style.display = 'block';

    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector('[data-section="dashboard"]').classList.add('active');
    document.getElementById('pageTitle').textContent = 'Dashboard';

    if (window.doughnutChart) window.doughnutChart.destroy();
    if (window.barChart) window.barChart.destroy();
}

// Sidebar toggle for mobile
document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('active');
});