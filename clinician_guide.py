from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfutils
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime
import os

def register_fonts():
    try:
        pdfmetrics.registerFont(TTFont('TimesRoman', 'times.ttf'))
        pdfmetrics.registerFont(TTFont('TimesBold', 'timesbd.ttf'))
        return 'TimesRoman', 'TimesBold'
    except:
        return 'Times-Roman', 'Times-Bold'

class ClinicianGuideTemplate:
    def on_first_page(self, canvas, doc):
        canvas.saveState()
        # Add logo if exists (centered)
        if os.path.exists('logo-icon-negative.png'):
            try:
                # Center the logo horizontally
                logo_x = (doc.width + doc.leftMargin + doc.rightMargin) / 2 - 20
                canvas.drawImage('logo-icon-negative.png', logo_x, 
                               doc.height + doc.topMargin - 60, 40, 40)
            except:
                pass
        
        # Footer
        canvas.setFont('Times-Roman', 10)
        canvas.setFillColor(HexColor('#666666'))
        canvas.drawString(doc.leftMargin, 30, "PsyDC - Psychological Data Collection & Validation Platform")
        canvas.drawRightString(doc.width + doc.leftMargin, 30, f"Generated: {datetime.now().strftime('%B %d, %Y')}")
        canvas.restoreState()
    
    def on_later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        canvas.setFillColor(HexColor('#666666'))
        canvas.drawString(doc.leftMargin, doc.height + doc.topMargin + 10, "PsyDC Clinician Guide")
        canvas.drawRightString(doc.width + doc.leftMargin, 30, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

def create_clinician_guide():
    font_normal, font_bold = register_fonts()
    
    doc = SimpleDocTemplate("PsyDC_Clinician_Guide.pdf", pagesize=A4,
                          topMargin=1.2*inch, bottomMargin=0.75*inch,
                          leftMargin=0.75*inch, rightMargin=0.75*inch)
    story = []
    
    # Styles
    title_style = ParagraphStyle('Title', fontName=font_bold, fontSize=20,
                               textColor=HexColor('#2c3e50'), alignment=TA_CENTER, spaceAfter=20)
    
    subtitle_style = ParagraphStyle('Subtitle', fontName=font_normal, fontSize=14,
                                  textColor=HexColor('#34495e'), alignment=TA_CENTER, spaceAfter=16)
    
    section_style = ParagraphStyle('Section', fontName=font_bold, fontSize=14,
                                 textColor=HexColor('#2c3e50'), spaceBefore=20, spaceAfter=12)
    
    normal_style = ParagraphStyle('Normal', fontName=font_normal, fontSize=11,
                                textColor=black, spaceAfter=6, leading=14, alignment=TA_JUSTIFY)
    
    bullet_style = ParagraphStyle('Bullet', fontName=font_normal, fontSize=11,
                                textColor=black, spaceAfter=4, leading=14, leftIndent=20)
    
    question_style = ParagraphStyle('Question', fontName=font_normal, fontSize=10,
                                  textColor=HexColor('#2c3e50'), spaceAfter=3, leading=13, leftIndent=15)
    
    response_style = ParagraphStyle('Response', fontName=font_normal, fontSize=10,
                                  textColor=HexColor('#7f8c8d'), spaceAfter=8, leading=12, leftIndent=25)
    
    # Title Page
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("PsyDC Clinician Guide", title_style))
    story.append(Paragraph("PHQ-9 Validation Platform Instructions", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Introduction
    story.append(Paragraph("INTRODUCTION", section_style))
    intro_text = """Welcome to the PsyDC (Psychological Data Collection) platform. This system enables clinicians to validate AI-generated PHQ-9 depression assessment scores by reviewing synthetic patient responses. Your expertise helps improve our AI scoring accuracy for clinical applications."""
    story.append(Paragraph(intro_text, normal_style))
    
    # PHQ-9 Questions Section
    story.append(Paragraph("PHQ-9 ASSESSMENT QUESTIONS", section_style))
    story.append(Paragraph("Over the last 2 weeks, how often have you been bothered by any of the following problems?", normal_style))
    
    questions = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless", 
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading the newspaper or watching television",
        "Moving or speaking so slowly that other people could have noticed. Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead, or of hurting yourself in some way"
    ]
    
    for i, question in enumerate(questions, 1):
        story.append(Paragraph(f"{i}. {question}", question_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    # Scoring Scale
    scale_data = [
        ['Response', 'Score', 'Description'],
        ['Not at all', '0', 'No symptoms present'],
        ['Several days', '1', 'Symptoms present 1-6 days'],
        ['More than half the days', '2', 'Symptoms present 7+ days'],
        ['Nearly every day', '3', 'Symptoms present 12+ days']
    ]
    
    scale_table = Table(scale_data, colWidths=[2*inch, 0.8*inch, 2.2*inch])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#ecf0f1')),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTNAME', (0, 1), (-1, -1), font_normal),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(scale_table)
    
    # Severity Levels
    story.append(Spacer(1, 0.2*inch))
    severity_data = [
        ['Total Score', 'Severity Level', 'Clinical Interpretation'],
        ['0-4', 'None/Minimal', 'No significant depression'],
        ['5-9', 'Mild', 'Mild depression symptoms'],
        ['10-14', 'Moderate', 'Moderate depression'],
        ['15-19', 'Moderately Severe', 'Moderately severe depression'],
        ['20-27', 'Severe', 'Severe depression']
    ]
    
    severity_table = Table(severity_data, colWidths=[1.2*inch, 1.5*inch, 2.3*inch])
    severity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), font_bold),
        ('FONTNAME', (0, 1), (-1, -1), font_normal),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(severity_table)
    
    # Sample Patient Responses
    story.append(PageBreak())
    story.append(Paragraph("SAMPLE PATIENT RESPONSES", section_style))
    
    # Sample 1 - Mild Depression
    story.append(Paragraph("Sample 1: Mild Depression (AI Score: 7)", ParagraphStyle('SampleHeader', fontName=font_bold, fontSize=12, textColor=HexColor('#e67e22'), spaceAfter=8)))
    
    sample1_responses = [
        "I've been a little down lately, though I can still laugh at things sometimes.",
        "Some of the stuff I used to love doesn't excite me quite as much.",
        "My sleep's been hit or miss—some nights I just can't stay asleep.",
        "I feel tired more often than I used to.",
        "I've been eating less, not much appetite most days.",
        "I sometimes feel like I'm not doing enough or letting people down.",
        "My focus slips sometimes, especially during long meetings.",
        "I get a bit antsy but nothing serious.",
        "No thoughts of self-harm—just a bit low."
    ]
    
    for i, response in enumerate(sample1_responses, 1):
        story.append(Paragraph(f"Q{i}: {response}", response_style))
    
    story.append(Spacer(1, 0.15*inch))
    
    # Sample 2 - Moderate Depression  
    story.append(Paragraph("Sample 2: Moderate Depression (AI Score: 13)", ParagraphStyle('SampleHeader', fontName=font_bold, fontSize=12, textColor=HexColor('#f39c12'), spaceAfter=8)))
    
    sample2_responses = [
        "I've been feeling sad and empty more days than not.",
        "Things I used to love—music, movies—don't bring much joy anymore.",
        "My sleep is really inconsistent; sometimes I oversleep, other times I can't fall asleep at all.",
        "I'm tired nearly every day, even when I haven't done much.",
        "My appetite changes; some days I barely eat.",
        "I often feel like a failure, like I'm disappointing everyone.",
        "It's hard to focus—my thoughts wander constantly.",
        "I feel sluggish, like moving through mud.",
        "I've had fleeting thoughts about life not being worth much, but I wouldn't act on them."
    ]
    
    for i, response in enumerate(sample2_responses, 1):
        story.append(Paragraph(f"Q{i}: {response}", response_style))
    
    story.append(Spacer(1, 0.15*inch))
    
    # Sample 3 - Severe Depression
    story.append(Paragraph("Sample 3: Severe Depression (AI Score: 24)", ParagraphStyle('SampleHeader', fontName=font_bold, fontSize=12, textColor=HexColor('#e74c3c'), spaceAfter=8)))
    
    sample3_responses = [
        "I can't remember the last time I felt joy or excitement about anything.",
        "I wake up with dread every morning, feeling hopeless about the day ahead.",
        "My sleep is terrible — I either stay awake all night or sleep for 14 hours and still feel tired.",
        "I have no energy, like my body's made of lead.",
        "I've stopped eating properly; sometimes I go a whole day without realizing it.",
        "I feel like a complete failure, like I'm a burden to everyone around me.",
        "I can't focus on anything — even watching TV feels impossible.",
        "I move and speak slowly; sometimes I just sit in silence for hours.",
        "I often think about ending my life because I don't see things improving."
    ]
    
    for i, response in enumerate(sample3_responses, 1):
        story.append(Paragraph(f"Q{i}: {response}", response_style))
    
    # Platform Instructions
    story.append(PageBreak())
    story.append(Paragraph("PLATFORM USAGE INSTRUCTIONS", section_style))
    
    # Getting Started
    story.append(Paragraph("Getting Started", ParagraphStyle('SubSection', fontName=font_bold, fontSize=12, textColor=HexColor('#2c3e50'), spaceAfter=8)))
    
    getting_started = [
        "Visit the PsyDC platform website",
        "Read the detailed information and guidelines (required)",
        "Enter your name and provide consent to participate",
        "Click 'Let's PsyDC' to begin the validation process"
    ]
    
    for step in getting_started:
        story.append(Paragraph(f"• {step}", bullet_style))
    
    # Validation Process
    story.append(Paragraph("Validation Process", ParagraphStyle('SubSection', fontName=font_bold, fontSize=12, textColor=HexColor('#2c3e50'), spaceAfter=8, spaceBefore=15)))
    
    validation_steps = [
        "Review patient responses: Each screen shows one patient's answers to all 9 PHQ-9 questions",
        "Check AI scoring: The AI-calculated score (0-27) and severity level are displayed",
        "Use PHQ-9 reference: Click 'Show PHQ-9 Questions' button to view the original questions",
        "Make validation decision: Click 'Valid' if you agree with the AI assessment, or 'Not Valid' if you disagree",
        "Provide corrections (if invalid): Enter your corrected score, severity level, and reason for the change",
        "Navigate between patients: Use Previous/Next buttons to review cases in any order"
    ]
    
    for step in validation_steps:
        story.append(Paragraph(f"• {step}", bullet_style))
    
    # Validation Guidelines
    story.append(Paragraph("Validation Guidelines", ParagraphStyle('SubSection', fontName=font_bold, fontSize=12, textColor=HexColor('#2c3e50'), spaceAfter=8, spaceBefore=15)))
    
    guidelines = [
        "Consider the overall pattern of responses rather than individual answers",
        "Look for consistency between symptom severity and frequency descriptions",
        "Pay attention to functional impairment indicators in patient responses",
        "Consider cultural and individual variations in symptom expression",
        "When in doubt, err on the side of clinical caution",
        "Provide specific, clear reasons when marking assessments as invalid"
    ]
    
    for guideline in guidelines:
        story.append(Paragraph(f"• {guideline}", bullet_style))
    
    # Technical Features
    story.append(Paragraph("Platform Features", ParagraphStyle('SubSection', fontName=font_bold, fontSize=12, textColor=HexColor('#2c3e50'), spaceAfter=8, spaceBefore=15)))
    
    features = [
        "Progress tracking: Your progress is automatically saved and can be resumed later",
        "PHQ-9 reference panel: Toggle button to show/hide the original questions",
        "Export functionality: Generate PDF report of all your validations upon completion",
        "Mobile compatibility: Platform works on tablets and smartphones",
        "Data security: All patient data is synthetic; no real patient information is used"
    ]
    
    for feature in features:
        story.append(Paragraph(f"• {feature}", bullet_style))
    
    # Important Notes
    story.append(Paragraph("Important Notes", ParagraphStyle('SubSection', fontName=font_bold, fontSize=12, textColor=HexColor('#c0392b'), spaceAfter=8, spaceBefore=15)))
    
    notes = [
        "All patient responses are AI-generated synthetic data, not real patient information",
        "Your validations help improve AI accuracy for future clinical applications",
        "Complete all 350 validations to generate your final report",
        "Contact support if you encounter technical issues: sayar.basu.cse26@heritageit.edu.in"
    ]
    
    for note in notes:
        story.append(Paragraph(f"• {note}", bullet_style))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Thank you for your participation in improving AI-assisted mental health assessment!", 
                          ParagraphStyle('Footer', fontName=font_normal, fontSize=11, textColor=HexColor('#7f8c8d'), 
                                       alignment=TA_CENTER, spaceAfter=10)))
    
    # Build PDF
    page_template = ClinicianGuideTemplate()
    doc.build(story, onFirstPage=page_template.on_first_page, onLaterPages=page_template.on_later_pages)
    print("Clinician guide generated: PsyDC_Clinician_Guide.pdf")

if __name__ == "__main__":
    create_clinician_guide()