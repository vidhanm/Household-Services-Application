from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS
from os import path
from cache import cache
from celery_config import init_celery
import redis
import os

# Create the extensions
db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    
    
    app.config['CACHE_TYPE'] = 'redis'
    app.config['CACHE_REDIS_HOST'] = redis_host
    app.config['CACHE_REDIS_PORT'] = redis_port
    app.config['CACHE_REDIS_DB'] = 0
    
    cache.init_app(app)
    redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

    app.config['EXPORT_FOLDER'] = '/database/export_files'

    app.config['CELERY_BROKER_URL'] = f'redis://{redis_host}:6379/2'
    app.config['CELERY_RESULT_BACKEND'] = f'redis://{redis_host}:6379/3'
    
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MAD2.sqlite3'
    app.config['SECRET_KEY'] = 'your_secret_key_here' 
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'jwt_secret_key_here' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    # Initialize extensions

    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    

    # Configure login manager
    login_manager.login_view = 'auth.login'

    # Initialize Flask-RESTful
    api = Api(app)

    with app.app_context():
        from models import User, Service, Professional, ServiceRequest # Import the models
        db.create_all()

    # Import and register resources
    from resources.auth import UserRegister, UserLogin, UserLogout, TokenRefresh, ResetPassword, ForgotPassword
    from resources.admin import AdminDashboard, ServiceManagement, ProfessionalApproval, GetCertification, AdminDashboardStats, AdminAnalytics, AdminUsers, ExportServices
    from resources.customer import CustomerServiceRequests, SearchServices, OngoingServices,CompletedServices, CustomerFeedbackApproval
    from resources.professional import ProfessionalDashboard,ProfessionalHistory

    # Add resources to the API
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(AdminDashboard, '/admin/dashboard')
    api.add_resource(AdminDashboardStats, '/admin/dashboard/stats')
    api.add_resource(AdminAnalytics, '/admin/analytics/data')
    api.add_resource(AdminUsers, '/admin/users', '/admin/users/<int:user_id>')
    api.add_resource(ServiceManagement, '/admin/services', '/admin/services/<int:service_id>')
    api.add_resource(CustomerServiceRequests, '/api/customer/service-requests', '/api/customer/service-requests/<int:request_id>')
    api.add_resource(SearchServices, '/customer/services/search')
    api.add_resource(ProfessionalDashboard, '/professional/dashboard')
    api.add_resource(ProfessionalHistory, '/professional/history')
    api.add_resource(OngoingServices, '/api/customer/ongoing-services')
    api.add_resource(CompletedServices, '/api/customer/completed-services')
    api.add_resource(CustomerFeedbackApproval, '/api/customer-feedback/<int:request_id>')
    api.add_resource(ProfessionalApproval, '/admin/professionals/pending', '/admin/professionals/approve/<int:professional_id>')
    api.add_resource(GetCertification, '/api/admin/certificate/<int:professional_id>')
    api.add_resource(ResetPassword, '/reset-password')
    api.add_resource(ForgotPassword, '/forgot-password')
    api.add_resource(ExportServices, '/admin/export-services')
    # Add Mail configuration
    # app.config.update(MAIL_CONFIG)
    # mail.init_app(app)

    return app

# Create the app
app = create_app()
celery = init_celery(app)
