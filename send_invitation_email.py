import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

# Email configuration
SENDER_EMAIL = "sayar.basu.cse26@heritageit.edu.in"
APP_PASSWORD = "mujz dzqu tsxu cqkq"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_invitation_email(recipient_email, counselor_name, sender_name="Sayar Basu", sender_title="Research Student", sender_institution="Heritage Institute of Technology"):
    """Send PsyDC invitation email to counselor"""
    
    # Create message
    msg = MIMEMultipart('related')
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = "PsyDC Research Invitation - Your Expertise Needed for Psychological Data Validation"
    
    # Read HTML template
    with open('counselor_invitation_email.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Replace placeholders
    html_content = html_content.replace('[Counselor Name]', counselor_name)
    html_content = html_content.replace('[Your Name]', sender_name)
    html_content = html_content.replace('[Your Title/Position]', sender_title)
    html_content = html_content.replace('[Institution/Organization]', sender_institution)
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Attach logo
    if os.path.exists('logo-icon.png'):
        with open('logo-icon.png', 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data)
        image.add_header('Content-ID', '<logo-icon.png>')
        image.add_header('Content-Disposition', 'inline', filename='logo-icon.png')
        msg.attach(image)
    
    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent successfully to {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage
    recipient = input("Enter counselor's email: ")
    name = input("Enter counselor's name: ")
    
    send_invitation_email(recipient, name)