from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import db

class User(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'customer', 'professional'
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    base_duration = db.Column(db.Integer, default=60)  # Base duration in minutes
    price_per_hour = db.Column(db.Float)  # Additional price per hour
    time_required = db.Column(db.Integer)
    description = db.Column(db.Text)
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    proposed_service = db.Column(db.String(100), nullable=False)  # What professional proposes
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=True)  # Admin assigned service
    assigned_service = db.Column(db.String(80))  # New column
    experience = db.Column(db.Integer, nullable=False)
    document_path = db.Column(db.String(255), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    approval_date = db.Column(db.DateTime)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=True)
    service_type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    service_status = db.Column(db.String(50), default='requested')
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    remarks = db.Column(db.Text)
    rating = db.Column(db.Float)
    feedback = db.Column(db.Text)
