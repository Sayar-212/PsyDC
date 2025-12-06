import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
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
    msg['Subject'] = "Invitation: Psy Dataset Validation and Cross Checking of AI generated Scores of Synthetic Data."
    
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
    
    # Note: logo attachment removed as per request (no inline logo will be attached)
    
    # Attach PDFs
    pdf_files = ['PsyDC_Clinician_Guide.pdf', 'PHQ9_Research_Report.pdf']
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            with open(pdf_file, 'rb') as f:
                pdf_data = f.read()
            pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_file)
            msg.attach(pdf_attachment)
            print(f"📎 Attached: {pdf_file}")
    
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
    print("=== PsyDC Email Sender ===")
    print("\nEnter TO recipients (2 emails):")
    to_email_1 = input("TO Email 1: ").strip()
    to_email_2 = input("TO Email 2: ").strip()
    
    print("\nEnter CC recipients (4 emails):")
    cc_email_1 = input("CC Email 1: ").strip()
    cc_email_2 = input("CC Email 2: ").strip()
    cc_email_3 = input("CC Email 3: ").strip()
    cc_email_4 = input("CC Email 4: ").strip()
    
    name = input("\nEnter counselor's name: ").strip()
    
    to_emails = [to_email_1, to_email_2]
    cc_emails = [cc_email_1, cc_email_2, cc_email_3, cc_email_4]
    
    # Create message
    msg = MIMEMultipart('related')
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(to_emails)
    msg['Cc'] = ', '.join(cc_emails)
    msg['Subject'] = "Invitation: Psy Dataset Validation and Cross Checking of AI generated Scores of Synthetic Data."
    
    # Read HTML template
    with open('counselor_invitation_email.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Attach HTML content
    msg.attach(MIMEText(html_content, 'html'))
    
    # Attach PDFs
    pdf_files = ['PsyDC_Clinician_Guide.pdf', 'PHQ9_Research_Report.pdf']
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            with open(pdf_file, 'rb') as f:
                pdf_data = f.read()
            pdf_attachment = MIMEApplication(pdf_data, _subtype='pdf')
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_file)
            msg.attach(pdf_attachment)
            print(f"📎 Attached: {pdf_file}")
    
    # Send email
    try:
        all_recipients = to_emails + cc_emails
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, all_recipients, msg.as_string())
        server.quit()
        print(f"\n✅ Email sent successfully!")
        print(f"TO: {', '.join(to_emails)}")
        print(f"CC: {', '.join(cc_emails)}")
    except Exception as e:
        print(f"\n❌ Failed to send email: {str(e)}")
