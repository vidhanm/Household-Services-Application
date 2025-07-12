from flask_sqlalchemy import SQLAlchemy
from config import db
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Professional
from pprint import pprint
import os
from werkzeug.utils import secure_filename
from utils.otp import generate_otp, store_otp, verify_otp, send_otp_email
from cache import cache

UPLOAD_FOLDER = 'uploads/professional_docs'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UserRegister(Resource):
    def post(self):
        try:
            role = request.form.get('role') if request.form else request.json.get('role')
            
            if role == 'customer':
                return self.register_customer()
            elif role == 'professional':
                return self.register_professional()
            else:
                return {"message": "Invalid role specified"}, 400
                
        except Exception as e:
            db.session.rollback()
            return {"message": f"Registration failed: {str(e)}"}, 500
            
    def register_customer(self):
        data = request.json
        if not all(k in data for k in ['username', 'email', 'phone', 'password']):
            return {"message": "Missing required fields"}, 400
            
        # Create customer user
        hashed_password = generate_password_hash(data['password'])
        new_user = User(
            username=data['username'],
            password=hashed_password,
            email=data['email'],
            phone=data['phone'],
            role='customer'
        )
        
        db.session.add(new_user)
        db.session.commit()
        return {"message": "Customer registration successful"}, 201
        
    def register_professional(self):
        # Validate required fields
        required_fields = ['username', 'email', 'phone', 'password', 'age', 'service', 'experience']
        for field in required_fields:
            if not request.form.get(field):
                return {"message": f"Missing required field: {field}"}, 400
                
        # Handle document upload
        if 'document' not in request.files:
            return {"message": "No document file provided"}, 400
            
        document = request.files['document']
        if document.filename == '':
            return {"message": "No selected file"}, 400
            
        if not allowed_file(document.filename):
            return {"message": "Invalid file type"}, 400
            
        # Save document
        filename = secure_filename(f"{request.form.get('username')}_{document.filename}")
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        document_path = os.path.join(UPLOAD_FOLDER, filename)
        document.save(document_path)
        
        # Create professional user
        hashed_password = generate_password_hash(request.form.get('password'))
        new_user = User(
            username=request.form.get('username'),
            password=hashed_password,
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            role='professional'
        )
        
        db.session.add(new_user)
        db.session.flush()  # Get user_id before committing
        
        # Create professional profile
        new_professional = Professional(
            user_id=new_user.id,
            age=request.form.get('age'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            proposed_service=request.form.get('service'),
            experience=request.form.get('experience'),
            document_path=filename,
            is_approved=False
        )
        
        db.session.add(new_professional)
        db.session.commit()
        
        return {"message": "Professional registration successful. Pending admin approval."}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            # Print user data for verification
            print(f"User data: id={user.id}, username={user.username}, email={user.email}, role={user.role}")
            
            claims = {
                'role': user.role,
                'email': user.email,
                'username': user.username,
                'sub': user.id  # Ensure sub claim is set to user ID
            }
            print(f"Token claims: {claims}")
            
            access_token = create_access_token(
                identity=user.id,
                additional_claims=claims
            )
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user_role': user.role,
                'user_email': user.email,  # Include these in response
                'user_name': user.username
            }, 200
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # You might want to blacklist the token here
        return {'message': 'Successfully logged out'}, 200

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user)
        return {'access_token': new_token}, 200

class ForgotPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        args = parser.parse_args()
        
        user = User.query.filter_by(email=args['email']).first()
        if not user:
            return {"message": "Email not found"}, 404
            
        otp = generate_otp()
        if store_otp(args['email'], otp) and send_otp_email(args['email'], otp):
            return {"message": "OTP sent successfully"}, 200
        return {"message": "Failed to send OTP"}, 500

class ResetPassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('otp', type=str, required=True)
        parser.add_argument('new_password', type=str, required=True)
        args = parser.parse_args()
        
        if not verify_otp(args['email'], args['otp']):
            return {"message": "Invalid or expired OTP"}, 400
            
        user = User.query.filter_by(email=args['email']).first()
        if not user:
            return {"message": "User not found"}, 404
            
        user.password = generate_password_hash(args['new_password'])
        db.session.commit()
        
        return {"message": "Password reset successfully"}, 200
