from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import smtplib
import base64
# Initialize Flask-Mail
SMTP_SERVER_HOST = "localhost"
SMTP_SERVER_PORT = 1025
SENDER_ADDRESS = "donotreply@homeservice.com"
SENDER_PASSWORD = "password"

def send_mail():
      # Compose email
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = "random@gmail.com"
    msg['Subject'] = 'Pending Service Request Reminder'
    
    # Email body
    body = f"""
    Dear
    
    You have a pending service request that requires your attention:
    
    Service: 
    Request Date:
    Status: Pending
    
    Please complete the service on time.
    
    Best regards,
    Home Service Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
        smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
        smtp_server.send_message(msg)
        smtp_server.quit()
    except Exception as e:
        print(f"Failed to send reminder email: {e}")        
        
send_mail()