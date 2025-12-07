import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
SENDER_EMAIL = "sayar.basu.cse26@heritageit.edu.in"
APP_PASSWORD = "mujz dzqu tsxu cqkq"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Recipient
RECIPIENT_EMAIL = "adib.shams.cse26@heritageit.edu.in"
RECIPIENT_NAME = "Adib Shams"

print("=== PsyDC QA Test Email Sender ===\n")

# Create message
msg = MIMEMultipart('related')
msg['From'] = SENDER_EMAIL
msg['To'] = RECIPIENT_EMAIL
msg['Subject'] = "PsyDC QA Testing Invitation - Access Token Included"

# Read HTML template
with open('qa_tester_invitation_email.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Attach HTML content
msg.attach(MIMEText(html_content, 'html'))

# Send email
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()
    print("[SUCCESS] QA Test invitation email sent successfully!")
    print(f"TO: {RECIPIENT_EMAIL}")
    print(f"Subject: PsyDC QA Testing Invitation - Access Token Included")
except Exception as e:
    print(f"[ERROR] Failed to send email: {str(e)}")
