from flask import send_from_directory
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Service, Professional, ServiceRequest
from config import db  # Import db from config.py instead of app.py
from datetime import datetime, timedelta
from flask import request, jsonify, make_response
from sqlalchemy import func, and_

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403
        
        customers = User.query.filter_by(role='customer').count()
        professionals = Professional.query.count()
        services = Service.query.count()

        return {
            "customers": customers,
            "professionals": professionals,
            "services": services
        }

class ServiceManagement(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403
            
        services = Service.query.all()
        return {
            "services": [{
                "id": service.id,
                "name": service.name,
                "price": service.price,
                "time_required": service.time_required,
                "description": service.description,
                "rating": service.rating,
                "rating_count": service.rating_count
            } for service in services]
        }

    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('time_required', type=int, required=True)
        parser.add_argument('description', type=str)
        parser.add_argument('rating', type=float)
        parser.add_argument('rating_count', type=int)
        data = parser.parse_args()

        new_service = Service(**data)
        db.session.add(new_service)
        db.session.commit()

        return {"message": "Service created successfully", "id": new_service.id}, 201

    @jwt_required()
    def put(self, service_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403

        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('price', type=float)
        parser.add_argument('time_required', type=int)
        parser.add_argument('description', type=str)
        data = parser.parse_args()

        for key, value in data.items():
            if value is not None:
                setattr(service, key, value)

        db.session.commit()

        return {"message": "Service updated successfully"}

    @jwt_required()
    def delete(self, service_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403

        service = Service.query.get(service_id)
        if not service:
            return {"message": "Service not found"}, 404

        db.session.delete(service)
        db.session.commit()

        return {"message": "Service deleted successfully"}

class ProfessionalApproval(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403

        pending_professionals = Professional.query.filter_by(is_approved=False).all()
        print(pending_professionals)
        return {
            "pending_professionals": [{
                "id": pending_professional.id,
                "user_id": pending_professional.user_id,
                "name": User.query.get(pending_professional.user_id).username,
                "service": pending_professional.assigned_service,
                "experience": pending_professional.experience,
                "document_path": pending_professional.document_path
            } for pending_professional in pending_professionals]
        }

    @jwt_required()
    def post(self, professional_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('approved', type=bool, required=True)
        parser.add_argument('service_name', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('time_required', type=int, required=True)
        data = parser.parse_args()

        professional = Professional.query.get(professional_id)
        if not professional:
            return {"message": "Professional not found"}, 404

        if data['approved']:
            # Create or get existing service
            service = Service.query.filter_by(name=data['service_name']).first()
            if not service:
                service = Service(
                    name=data['service_name'],
                    price=data['price'],
                    time_required=data['time_required']
                )
                db.session.add(service)
                db.session.flush()

            professional.is_approved = True
            professional.assigned_service = data['service_name']
            professional.approval_date = datetime.utcnow()
            db.session.commit()

            return {"message": "Professional approved and service created successfully"}
        else:
            db.session.delete(professional)
            user = User.query.get(professional.user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "Professional registration rejected"}

class ExportServices(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return {"message": "Access denied"}, 403

        # Start async job for CSV export
        export_task.delay()  # This would be your Celery task
        return {"message": "Export job started"}, 202

class GetCertification(Resource):
    
    def get(self, professional_id):
        #user_id = get_jwt_identity()
        #user = User.query.get(user_id)
        #if user.role != 'admin':
        #return {"message": "Access denied"}, 403
        professional = Professional.query.get(professional_id)
        return send_from_directory('uploads/professional_docs', professional.document_path)

class AdminDashboardStats(Resource):
    @jwt_required()
    def get(self):
        # Check if user is admin
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return make_response(jsonify({"message": "Admin access required"}), 403)
        
        # Get total users
        total_users = User.query.count()
        
        # Get pending verifications (professionals awaiting approval)
        pending_verifications = Professional.query.filter_by(is_approved=False).count()
        
        # Get active services
        active_services = Service.query.count()
        
        # Get total revenue (from completed service requests)
        total_revenue = db.session.query(func.sum(ServiceRequest.price))\
            .filter(ServiceRequest.service_status == 'completed')\
            .scalar() or 0
            
        return {
            'total_users': total_users,
            'pending_verifications': pending_verifications,
            'active_services': active_services,
            'total_revenue': float(total_revenue)
        }

class AdminAnalytics(Resource):
    @jwt_required()
    def get(self):
        # Check if user is admin
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_admin:
            return make_response(jsonify({"message": "Admin access required"}), 403)
        
        # MOCK DATA for demonstration purposes
        # In a real application, this would come from database queries
        
        # 1. User Registration Growth - Last 6 months
        users_growth = [
            {"month": "2023-07", "count": 3},
            {"month": "2023-08", "count": 5},
            {"month": "2023-09", "count": 8},
            {"month": "2023-10", "count": 12},
            {"month": "2023-11", "count": 15},
            {"month": "2023-12", "count": 20}
        ]
        
        # 2. User Distribution by Role
        user_roles = [
            {"role": "admin", "count": 1},
            {"role": "customer", "count": 15},
            {"role": "professional", "count": 4}
        ]
        
        # 3. Most Popular Services
        popular_services = [
            {"service": "Plumbing", "count": 28},
            {"service": "Electrical", "count": 23},
            {"service": "Cleaning", "count": 18},
            {"service": "Painting", "count": 15},
            {"service": "Carpentry", "count": 10}
        ]
        
        # 4. Service Revenue Analysis
        service_revenue = [
            {"service": "Plumbing", "revenue": 28000.0},
            {"service": "Electrical", "revenue": 23500.0},
            {"service": "Cleaning", "revenue": 15000.0},
            {"service": "Painting", "revenue": 18500.0},
            {"service": "Carpentry", "revenue": 12000.0}
        ]
        
        # 5. Service Request Status Distribution
        status_distribution = [
            {"status": "requested", "count": 12},
            {"status": "accepted", "count": 8},
            {"status": "in progress", "count": 5},
            {"status": "completed", "count": 25},
            {"status": "cancelled", "count": 3}
        ]
        
        # 6. Professional Performance - Top 5 rated
        professional_ratings = [
            {"name": "John Smith", "rating": 4.8, "count": 15},
            {"name": "Alice Johnson", "rating": 4.7, "count": 12},
            {"name": "Bob Williams", "rating": 4.5, "count": 10},
            {"name": "Emily Davis", "rating": 4.2, "count": 8},
            {"name": "Michael Brown", "rating": 4.0, "count": 6}
        ]
        
        # 7. Monthly Revenue Trend - Last 6 months
        revenue_trend = [
            {"month": "2023-07", "revenue": 12000.0},
            {"month": "2023-08", "revenue": 15500.0},
            {"month": "2023-09", "revenue": 18000.0},
            {"month": "2023-10", "revenue": 22500.0},
            {"month": "2023-11", "revenue": 25000.0},
            {"month": "2023-12", "revenue": 32000.0}
        ]
            
        return {
            'users_growth': users_growth,
            'user_roles': user_roles,
            'popular_services': popular_services,
            'service_revenue': service_revenue,
            'status_distribution': status_distribution,
            'professional_ratings': professional_ratings,
            'revenue_trend': revenue_trend
        }

class AdminUsers(Resource):
    @jwt_required()
    def get(self):
        # Check if user is admin
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or user.role != 'admin':
            return make_response(jsonify({"message": "Admin access required"}), 403)
        
        # Get all users with pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Optional search parameter
        search_term = request.args.get('search', '')
        
        # Query with search
        if search_term:
            users_query = User.query.filter(
                User.username.like(f'%{search_term}%') | 
                User.email.like(f'%{search_term}%')
            )
        else:
            users_query = User.query
            
        # Get paginated results
        users_paginated = users_query.paginate(page=page, per_page=per_page)
        total_users = users_query.count()
        
        # Format user data
        users_list = []
        for user in users_paginated.items:
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "date_created": user.date_created.strftime('%Y-%m-%d %H:%M:%S') if user.date_created else None,
                "is_active": True  # You can modify this based on your user model
            }
            
            # Add role-specific information
            if user.role == 'professional':
                professional = Professional.query.filter_by(user_id=user.id).first()
                if professional:
                    user_data["professional_info"] = {
                        "is_approved": professional.is_approved,
                        "assigned_service": professional.assigned_service,
                        "experience": professional.experience
                    }
            
            users_list.append(user_data)
        
        return {
            "users": users_list,
            "pagination": {
                "total": total_users,
                "pages": users_paginated.pages,
                "page": page,
                "per_page": per_page,
                "has_next": users_paginated.has_next,
                "has_prev": users_paginated.has_prev
            }
        }
    
    @jwt_required()
    def put(self, user_id):
        # Update user information
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return make_response(jsonify({"message": "Admin access required"}), 403)
            
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
            
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('role', type=str)
        parser.add_argument('is_active', type=bool)
        data = parser.parse_args()
        
        # Update fields if provided
        for key, value in data.items():
            if value is not None:
                setattr(user, key, value)
                
        db.session.commit()
        return make_response(jsonify({"message": "User updated successfully"}), 200)
    
    @jwt_required()
    def delete(self, user_id):
        # Delete a user
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.role != 'admin':
            return make_response(jsonify({"message": "Admin access required"}), 403)
            
        if int(current_user_id) == int(user_id):
            return make_response(jsonify({"message": "Cannot delete your own account"}), 400)
            
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)
            
        # Handle role-specific deletions
        if user.role == 'professional':
            professional = Professional.query.filter_by(user_id=user.id).first()
            if professional:
                db.session.delete(professional)
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        return make_response(jsonify({"message": "User deleted successfully"}), 200)

