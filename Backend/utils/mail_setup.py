from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import os
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
        
# send_mail()

def send_daily_mail(email, p_name, service_name, request_date):
    
    # Compose email
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = email
    msg['Subject'] = 'Pending Service Request Reminder'
    
    # Email body
    body = f"""
    Dear {p_name},
    
    You have a pending service request that requires your attention:
    
    Service: {service_name}
    Request Date: {request_date}
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

def send_monthly_activity_report(email, **kwargs):
    """
    Send monthly activity report to users or export CSV to admin.
    This function handles both the monthly report to users and CSV export to admin.
    
    Parameters:
    - email: recipient email address
    - kwargs: optional parameters, can include:
      - filename, filepath: for CSV export
      - user_name, report_period, total_services, etc.: for monthly reports
    """
    print(f"Sending email to {email} with params: {kwargs}")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = email
    
    # Check if this is a CSV export email (admin) or a monthly report (user)
    if 'filename' in kwargs and 'filepath' in kwargs:
        # This is a CSV export email
        msg['Subject'] = 'Service Requests Export'
        
        # Email body
        body = f"""
        Dear Admin,
        
        Attached is the export of completed service requests.
        
        Best regards,
        Home Service Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CSV
        try:
            with open(kwargs['filepath'], 'rb') as f:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(f.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', 'attachment', filename=kwargs['filename'])
                msg.attach(attachment)
        except Exception as e:
            print(f"Failed to attach file: {e}")
            
    else:
        # This is a monthly report email
        user_name = kwargs.get('user_name', 'Customer')
        report_period = kwargs.get('report_period', 'Last Month')
        total_services = kwargs.get('total_services', 0)
        total_completed = kwargs.get('total_completed', 0)
        total_pending = kwargs.get('total_pending', 0)
        avg_rating = kwargs.get('avg_rating', 0.0)
        user_completed = kwargs.get('user_completed', 0)
        user_pending = kwargs.get('user_pending', 0)
        
        msg['Subject'] = f'Monthly Activity Report - {report_period}'
        
        # Email body
        body = f"""
        Dear {user_name},
        
        Here is your monthly activity report for {report_period}:
        
        Platform Statistics:
        - Total Services Available: {total_services}
        - Total Completed Requests: {total_completed}
        - Total Pending Requests: {total_pending}
        - Average Service Rating: {avg_rating:.1f}/5.0
        
        Your Statistics:
        - Your Completed Requests: {user_completed}
        - Your Pending Requests: {user_pending}
        
        Thank you for using our services!
        
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
        print(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False