from flask_mail import Mail
import redis

mail = Mail()

# Redis Configuration
REDIS_HOST = 'your_ubuntu_server_ip'  # Change this to your Ubuntu server IP
REDIS_PORT = 6379
REDIS_DB = 0

# Redis client
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

# Mail Configuration
MAIL_CONFIG = {
    'MAIL_SERVER': 'localhost',  # Mailhog server
    'MAIL_PORT': 1025,          # Mailhog SMTP port
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': None,
    'MAIL_PASSWORD': None,
    'MAIL_DEFAULT_SENDER': 'noreply@yourapp.com'
} 