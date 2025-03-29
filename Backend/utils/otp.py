import random
import string
from datetime import datetime, timedelta
# from config.mail_config import redis_client
from flask_mail import Message
# from config.mail_config import mail

def generate_otp():
    """Generate a 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def store_otp(email, otp):
    """Store OTP in Redis with 5 minutes expiration"""
    redis_client.setex(f"otp:{email}", 300, otp)  # 300 seconds = 5 minutes

def verify_otp(email, otp):
    """Verify OTP from Redis"""
    stored_otp = redis_client.get(f"otp:{email}")
    if stored_otp and stored_otp == otp:
        redis_client.delete(f"otp:{email}")
        return True
    return False

def send_otp_email(email, otp):
    """Send OTP via email"""
    try:
        msg = Message(
            'Password Reset OTP',
            recipients=[email],
            body=f'Your OTP for password reset is: {otp}\nThis OTP will expire in 5 minutes.'
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False 