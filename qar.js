let currentPatient = 0;
let surveyData = null;
let qarData = {};
const SHEET_URL = 'https://script.google.com/macros/s/AKfycbx50oqzWv4JjYlZ8nipD76Zc-Ezc9kbRmyIuA-D8A-GusVuAO0NVD7b21WlSnh2NHdmkw/exec';

Promise.all([
    fetch('survey_data.json').then(res => res.json()),
    fetch(SHEET_URL + '?action=getQARProgress').then(res => res.json())
]).then(([data, progress]) => {
    surveyData = data;
    qarData = progress;
    
    for (let i = 0; i < surveyData.patients.length; i++) {
        const patientId = String(i + 1).padStart(3, '0');
        if (!qarData[patientId]) {
            currentPatient = i;
            break;
        }
    }
    
    updateDisplay();
});

function getSeverity(score) {
    if (score >= 0 && score <= 4) return 'Minimal Depression';
    if (score >= 5 && score <= 9) return 'Mild Depression';
    if (score >= 10 && score <= 14) return 'Moderate Depression';
    if (score >= 15 && score <= 19) return 'Moderately Severe Depression';
    if (score >= 20 && score <= 27) return 'Severe Depression';
    return '-';
}

function updateDisplay() {
    if (!surveyData) return;
    
    const totalPatients = surveyData.patients.length;
    const patientId = String(currentPatient + 1).padStart(3, '0');
    document.getElementById('patientNum').textContent = `Patient ${patientId}/${totalPatients}`;
    document.getElementById('patientId').textContent = `Patient ${patientId}`;
    
    const savedScore = qarData[patientId];
    document.getElementById('psyruleScore').value = savedScore || '';
    document.getElementById('severity').textContent = savedScore ? getSeverity(savedScore) : '-';
    
    document.getElementById('prevBtn').disabled = currentPatient === 0;
    document.getElementById('nextBtn').disabled = currentPatient === totalPatients - 1;
}

document.getElementById('saveBtn').addEventListener('click', () => {
    if (!surveyData) return;
    
    const score = document.getElementById('psyruleScore').value;
    if (score === '' || score < 0 || score > 27) {
        alert('Please enter a valid score between 0 and 27');
        return;
    }
    
    const patientId = String(currentPatient + 1).padStart(3, '0');
    const scoreInt = parseInt(score);
    qarData[patientId] = scoreInt;
    
    const patient = surveyData.patients[currentPatient];
    fetch(SHEET_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            action: 'saveQAR',
            patientId: patientId,
            validatedScore: scoreInt,
            validatedLevel: getSeverity(scoreInt),
            ruleScore: patient.ai_score,
            ruleLevel: patient.ai_severity,
            difference: Math.abs(scoreInt - patient.ai_score)
        })
    });
    
    if (currentPatient < surveyData.patients.length - 1) {
        currentPatient++;
        updateDisplay();
    } else {
        alert('All patients completed!');
    }
});

document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentPatient > 0) {
        currentPatient--;
        updateDisplay();
    }
});

document.getElementById('nextBtn').addEventListener('click', () => {
    if (!surveyData) return;
    if (currentPatient < surveyData.patients.length - 1) {
        currentPatient++;
        updateDisplay();
    }
});

document.getElementById('psyruleScore').addEventListener('input', (e) => {
    const score = parseInt(e.target.value);
    document.getElementById('severity').textContent = (score >= 0 && score <= 27) ? getSeverity(score) : '-';
});
