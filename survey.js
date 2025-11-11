const SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbx7ZsBZ0pKLzWNjSlm6a6HK7ySp1oK0tR6VVfi8mgUv6G42XOY9vDwVDm9nhrfl2PM-/exec';

let patients = [];
let questions = [];
let choices = [];
let currentIndex = 0;
let validations = [];
const clinicianName = localStorage.getItem('clinicianName');
const STORAGE_KEY = `psydc_progress_${clinicianName}`;

async function syncToSheet(validation) {
    const row = [
        validation.patient_id,
        validation.clinician,
        validation.validity,
        validation.ai_score,
        validation.ai_severity,
        validation.adjusted_score || '',
        validation.adjusted_severity || '',
        validation.reason || '',
        validation.timestamp
    ];
    
    try {
        await fetch(SCRIPT_URL, {
            method: 'POST',
            mode: 'no-cors',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row: row })
        });
    } catch (error) {
        console.error('Sheet sync failed:', error);
    }
}

document.getElementById('clinicianName').textContent = `Clinician: ${clinicianName}`;

// Show loading mask initially
document.getElementById('loadingMask').style.display = 'flex';

fetch('survey_data.json')
    .then(r => r.json())
    .then(data => {
        questions = data.questions;
        choices = data.choices;
        patients = data.patients;
        loadProgress();
    });

function loadProgress() {
    fetch(`${SCRIPT_URL}?action=getProgress&clinician=${encodeURIComponent(clinicianName)}`)
        .then(r => r.json())
        .then(data => {
            if (data && data.validations) {
                validations = data.validations;
                currentIndex = data.currentIndex || 0;
                showMessage(`Welcome back! Continuing from Patient ${currentIndex + 1}`);
            } else {
                showMessage('Starting fresh validation session');
            }
            showSurvey();
        })
        .catch(error => {
            console.log('No previous progress found, starting fresh');
            showMessage('Starting fresh validation session');
            showSurvey();
        });
}

function showMessage(message) {
    const loadingContent = document.querySelector('.loading-content');
    loadingContent.innerHTML = `
        <div class="spinner"></div>
        <h3>${message}</h3>
        <p>Loading survey interface...</p>
    `;
    
    setTimeout(() => {
        showSurvey();
    }, 1500);
}

function showSurvey() {
    document.getElementById('loadingMask').style.display = 'none';
    document.querySelector('.survey-container').style.display = 'block';
    loadPatient();
}

function saveProgress() {
    fetch(SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            action: 'saveProgress',
            clinician: clinicianName,
            validations,
            currentIndex,
            lastSaved: new Date().toISOString()
        })
    }).catch(error => {
        console.error('Progress save failed:', error);
    });
}

function loadPatient() {
    if (currentIndex >= patients.length) {
        showCompletionMessage();
        return;
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });

    const patient = patients[currentIndex];
    document.getElementById('patientNum').textContent = `Patient ${currentIndex + 1}/${patients.length}`;
    
    const answersList = document.getElementById('answersList');
    answersList.innerHTML = patient.answers.map((ans, i) => 
        `<div class="answer-item"><strong>Q${i + 1}:</strong> ${questions[i]}<br><em>${ans}</em></div>`
    ).join('');
    
    document.getElementById('aiScore').textContent = patient.ai_score;
    document.getElementById('aiSeverity').textContent = patient.ai_severity;
    document.getElementById('correctionForm').style.display = 'none';
    
    const existing = validations.find(v => v.patient_id === patient.id);
    if (existing) {
        if (existing.validity === 'Not Valid') {
            document.getElementById('correctionForm').style.display = 'block';
            document.getElementById('newScore').value = existing.adjusted_score;
            document.getElementById('newSeverity').value = existing.adjusted_severity;
            document.getElementById('reason').value = existing.reason;
        }
    }
}

document.getElementById('validBtn').addEventListener('click', () => {
    const patient = patients[currentIndex];
    validations = validations.filter(v => v.patient_id !== patient.id);
    validations.push({
        patient_id: patient.id,
        clinician: clinicianName,
        questions: questions,
        choices: choices,
        responses: patient.answers,
        ai_score: patient.ai_score,
        ai_severity: patient.ai_severity,
        validity: 'Valid',
        adjusted_score: null,
        adjusted_severity: null,
        reason: null,
        timestamp: new Date().toISOString()
    });
    syncToSheet(validations[validations.length - 1]);
    currentIndex++;
    saveProgress();
    loadPatient();
});

document.getElementById('invalidBtn').addEventListener('click', () => {
    document.getElementById('correctionForm').style.display = 'block';
    document.getElementById('correctionForm').scrollIntoView({ behavior: 'smooth', block: 'start' });
});

document.getElementById('submitCorrection').addEventListener('click', () => {
    const newScore = document.getElementById('newScore').value;
    const newSeverity = document.getElementById('newSeverity').value;
    const reason = document.getElementById('reason').value;
    
    if (!newScore || !newSeverity || !reason) {
        alert('Please fill all fields');
        return;
    }
    
    const patient = patients[currentIndex];
    validations = validations.filter(v => v.patient_id !== patient.id);
    validations.push({
        patient_id: patient.id,
        clinician: clinicianName,
        questions: questions,
        choices: choices,
        responses: patient.answers,
        ai_score: patient.ai_score,
        ai_severity: patient.ai_severity,
        validity: 'Not Valid',
        adjusted_score: parseInt(newScore),
        adjusted_severity: newSeverity,
        reason: reason,
        timestamp: new Date().toISOString()
    });
    
    syncToSheet(validations[validations.length - 1]);
    
    document.getElementById('newScore').value = '';
    document.getElementById('newSeverity').value = '';
    document.getElementById('reason').value = '';
    
    currentIndex++;
    saveProgress();
    loadPatient();
});

document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        saveProgress();
        loadPatient();
    }
});

document.getElementById('nextBtn').addEventListener('click', () => {
    if (currentIndex < patients.length - 1) {
        currentIndex++;
        saveProgress();
        loadPatient();
    }
});

function showCompletionMessage() {
    document.querySelector('.patient-card').innerHTML = `
        <div style="text-align: center; padding: 3rem;">
            <h2 style="font-size: 2.5rem; margin-bottom: 1rem; color: #4fc3f7;">🎉 Survey Complete!</h2>
            <p style="font-size: 1.2rem; margin-bottom: 2rem; color: rgba(255,255,255,0.8);">Thank you for completing all ${patients.length} validations!</p>
            <p style="font-size: 1rem; margin-bottom: 2rem; color: rgba(255,255,255,0.7);">Your valuable contribution will help improve our AI assessment system.</p>
            <div style="background: rgba(79, 195, 247, 0.1); padding: 2rem; border-radius: 8px; margin: 2rem 0;">
                <h3 style="color: #4fc3f7; margin-bottom: 1rem;">Next Step:</h3>
                <p style="text-align: center; line-height: 2;">Click "Export Results" button above to download the PDF report</p>
            </div>
            <p style="font-size: 0.9rem; color: rgba(255,255,255,0.6); margin-top: 2rem;">- PsyDC Team</p>
        </div>
    `;
}

document.getElementById('exportBtn').addEventListener('click', async () => {
    if (!window.jspdf) {
        alert('PDF library not loaded. Please refresh the page.');
        return;
    }
    
    const response = await fetch('survey_data.json');
    const surveyData = await response.json();
    
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Load logo
    const logoImg = new Image();
    logoImg.src = 'logo-icon-negative.png';
    await new Promise(resolve => logoImg.onload = resolve);
    
    // Watermark function
    const addWatermark = () => {
        doc.saveGraphicsState();
        doc.setGState(new doc.GState({ opacity: 0.25 }));
        doc.setTextColor(150, 150, 150);
        doc.setFontSize(60);
        doc.setFont('times', 'bold');
        doc.text('Psy', 105, 150, { align: 'center', angle: 45 });
        doc.restoreGraphicsState();
    };
    
    // Title Page
    addWatermark();
    doc.addImage(logoImg, 'PNG', 85, 30, 40, 40);
    doc.setFont('times', 'bold');
    doc.setFontSize(28);
    doc.text('PsyDC', 105, 85, { align: 'center' });
    doc.setFontSize(18);
    doc.text('Psy Data Collection Records', 105, 95, { align: 'center' });
    
    doc.setFont('times', 'normal');
    doc.setFontSize(14);
    doc.text(`Clinician: ${clinicianName}`, 105, 120, { align: 'center' });
    doc.setFontSize(12);
    doc.text(`Date: ${new Date().toLocaleDateString()}`, 105, 130, { align: 'center' });
    
    // Summary Box
    doc.setDrawColor(79, 195, 247);
    doc.setLineWidth(0.5);
    doc.rect(40, 150, 130, 40);
    doc.setFontSize(11);
    doc.text(`Total Reviewed: ${validations.length}`, 50, 165);
    doc.text(`Valid: ${validations.filter(v => v.validity === 'Valid').length}`, 50, 175);
    doc.text(`Not Valid: ${validations.filter(v => v.validity === 'Not Valid').length}`, 50, 185);
    
    // Patient Pages
    validations.forEach((v, i) => {
        doc.addPage();
        addWatermark();
        let y = 25;
        
        const patient = surveyData.patients.find(p => p.id === v.patient_id);
        const responses = v.responses || (patient ? patient.answers : []);
        
        doc.setFont('times', 'bold');
        doc.setFontSize(18);
        doc.text(`Set ${i + 1} - Patient ${v.patient_id}`, 105, y, { align: 'center' });
        y += 15;
        
        // Responses Box
        doc.setFont('times', 'bold');
        doc.setFontSize(12);
        doc.text('PHQ-9 Responses:', 20, y);
        y += 8;
        
        doc.setDrawColor(200, 200, 200);
        doc.setLineWidth(0.3);
        doc.rect(15, y - 5, 180, responses.length * 6 + 5);
        
        doc.setFont('times', 'normal');
        doc.setFontSize(10);
        responses.forEach((resp, idx) => {
            doc.text(`Q${idx + 1}: ${resp}`, 20, y);
            y += 6;
        });
        
        y += 10;
        
        // Results Box
        doc.setDrawColor(79, 195, 247);
        doc.setLineWidth(0.5);
        const boxHeight = v.validity === 'Not Valid' ? 45 : 25;
        doc.rect(15, y, 180, boxHeight);
        
        doc.setFont('times', 'bold');
        doc.setFontSize(11);
        y += 8;
        doc.text(`AI Score: ${v.ai_score}`, 20, y);
        y += 7;
        doc.text(`AI Severity: ${v.ai_severity}`, 20, y);
        y += 7;
        doc.text(`Validity: ${v.validity || 'Not Recorded'}`, 20, y);
        y += 7;
        
        if (v.validity === 'Not Valid' && v.adjusted_score) {
            doc.setTextColor(220, 53, 69);
            doc.text(`Adjusted Score: ${v.adjusted_score}`, 20, y);
            y += 7;
            doc.text(`Adjusted Severity: ${v.adjusted_severity}`, 20, y);
            y += 7;
            doc.setFont('times', 'italic');
            doc.setFontSize(10);
            const reasonLines = doc.splitTextToSize(`Reason: ${v.reason}`, 170);
            doc.text(reasonLines, 20, y);
            doc.setTextColor(0, 0, 0);
        }
    });
    
    const fileName = clinicianName ? `psydc_${clinicianName.replace(/\s+/g, '_')}_${Date.now()}.pdf` : `psydc_report_${Date.now()}.pdf`;
    doc.save(fileName);
    alert('✅ PDF report generated successfully!');
});

// PHQ-9 Questions Toggle Functionality
document.getElementById('toggleQuestions').addEventListener('click', () => {
    const panel = document.getElementById('questionsPanel');
    const button = document.getElementById('toggleQuestions');
    
    if (panel.style.display === 'none' || panel.style.display === '') {
        panel.style.display = 'block';
        button.textContent = 'Hide PHQ-9 Questions';
    } else {
        panel.style.display = 'none';
        button.textContent = 'Show PHQ-9 Questions';
    }
});

// Close questions panel when clicking outside
document.addEventListener('click', (e) => {
    const panel = document.getElementById('questionsPanel');
    const button = document.getElementById('toggleQuestions');
    
    if (panel.style.display === 'block' && 
        !panel.contains(e.target) && 
        !button.contains(e.target)) {
        panel.style.display = 'none';
        button.textContent = 'Show PHQ-9 Questions';
    }
});
