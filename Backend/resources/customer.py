from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Service, ServiceRequest, Professional
from config import db
from datetime import datetime
from http import HTTPStatus
from pprint import pprint
from cache import cache 


class SearchServices(Resource):
    @cache.cached(timeout=60, key_prefix='categories')
    def get(self):
        try:
            # Get only approved professionals
            approved_professionals = Professional.query.filter_by(is_approved=True).all()
            
            services = []
            for professional in approved_professionals:
                service = Service.query.filter_by(name=professional.assigned_service).first()
                if service:
                    services.append({
                        "id": professional.id,
                        "name": professional.assigned_service,
                        "price": service.price,
                        "rating": service.rating,
                        "ratingCount": service.rating_count,
                        "professional_id": professional.id,
                        "experience": professional.experience
                    })
            
            return services
            
        except Exception as e:
            return {"message": f"Error fetching services: {str(e)}"}, 500

class CustomerServiceHistory(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            if user.role != 'customer':
                return {"message": "Access denied"}, 403

            service_requests = ServiceRequest.query.filter_by(customer_id=user_id)\
                .order_by(ServiceRequest.date_of_request.desc())\
                .all()
            #print(service_requests)
            history = []
            for request in service_requests:
                professional = None
                #pprint(request)
                if request.professional_id:
                    user = User.query.get(request.professional_id)
                    #print(vars(user))
                    professional = Professional.query.join(User)\
                        .filter(Professional.id == request.professional_id)\
                        .filter(User.id == Professional.user_id)\
                        .first()
                    #pprint(vars(professional))
                    # print({"id": request.id,
                    # "serviceName": request.service_type,
                    # "professionalName": user.username if user else "Not Assigned",
                    # "phoneNo": user.phone if user else "N/A",
                    # "bookingDate": request.booking_date.strftime('%Y-%m-%d'),
                    # "bookingTime": request.booking_time.strftime('%H:%M'),
                    # "duration": f"{request.duration} minutes",
                    # "price": request.price,
                    # "status": request.service_status.capitalize(),
                    # "requestDate": request.date_of_request.strftime('%Y-%m-%d %H:%M'),
                    #     "remarks": request.remarks or "No remarks",
                    #      "professional": {
                    #         "experience": professional.experience if professional else None,
                    #         "description": professional.description if professional else None
                    #     } if professional else None
                    # })
                    history.append({
                    "id": request.id,
                    "serviceName": request.service_type,
                    "professionalName": user.username if user else "Not Assigned",
                    "phoneNo": user.phone if user else "N/A",
                    "bookingDate": request.booking_date.strftime('%Y-%m-%d'),
                    "bookingTime": request.booking_time.strftime('%H:%M'),
                    "duration": f"{request.duration} minutes",
                    "price": request.price,
                    "status": request.service_status.capitalize(),
                    "requestDate": request.date_of_request.strftime('%Y-%m-%d %H:%M'),
                    "remarks": request.remarks or "No remarks",
                    "professional": {
                        "experience": professional.experience if professional else None,
                        "description": professional.description if professional else None
                    } if professional else None
                })

            return {
                "message": "Service history retrieved successfully",
                "history": history
            }, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", e)  
            return {
                "message": "Failed to retrieve service history",
                "error": str(e)
            }, 500

class CustomerServiceRequests(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'customer':
            return {
                'message': 'Access denied. Customer role required.'
            }, HTTPStatus.FORBIDDEN

        parser = reqparse.RequestParser()
        parser.add_argument('requests', type=list, location='json', required=True)
        args = parser.parse_args()
        #print(args)
        try:
            created_requests = []
            for request_data in args['requests']:
                # Convert booking_date string to Date object
                iso_date = request_data['booking_date'].split('T')[0]
                booking_date = datetime.strptime(iso_date, '%Y-%m-%d').date()
                # Convert booking_time string to Time object
                booking_time = datetime.strptime(request_data['booking_time'], '%H:%M').time()
                
                # Create service request
                service_request = ServiceRequest(
                    customer_id=user_id,
                    service_type=request_data['service_type'],
                    price=request_data['price'],
                    booking_date=booking_date,
                    booking_time=booking_time,
                    duration=request_data['duration'],
                    service_status='requested'
                )
                
                db.session.add(service_request)
                created_requests.append(service_request)
            
            db.session.commit()
            
            return {
                'message': 'Service requests created successfully',
                'request_count': len(created_requests)
            }, HTTPStatus.CREATED

        except Exception as e:
            print("Error:", e)
            db.session.rollback()
            return {
                'message': 'Failed to create service requests',
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR

class CompleteService(Resource):
    @jwt_required()
    def post(self, request_id):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'customer':
            return {"message": "Access denied"}, 403

        service_request = ServiceRequest.query.get(request_id)
        if not service_request:
            return {"message": "Service request not found"}, 404

        if service_request.customer_id != user_id:
            return {"message": "Unauthorized to modify this request"}, 403

        if service_request.service_status != 'accepted':
            return {"message": "Can only complete accepted services"}, 400

        try:
            service_request.service_status = 'completed'
            db.session.commit()
            return {"message": "Service marked as completed"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to update service status", "error": str(e)}, 500
        

class CompletedServices(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            if user.role != 'customer':
                return {"message": "Access denied"}, 403

            service_requests = ServiceRequest.query.filter_by(
                customer_id=user_id,
                service_status='completed'
            ).order_by(ServiceRequest.date_of_request.desc()).all()

            completed = []
            for request in service_requests:
                professional = None
                if request.professional_id:
                    user = User.query.get(request.professional_id)
                    professional = Professional.query.filter_by(id=request.professional_id).first()
                    
                completed.append({
                    "id": request.id,
                    "serviceName": request.service_type,
                    "professionalName": user.username if user else "Not Available",
                    "phoneNo": user.phone if user else "N/A",
                    "bookingDate": request.booking_date.strftime('%Y-%m-%d'),
                    "bookingTime": request.booking_time.strftime('%H:%M'),
                    "completionDate": request.date_of_request.strftime('%Y-%m-%d'),
                    "duration": f"{request.duration} minutes",
                    "price": request.price,
                    "remarks": request.remarks or "No remarks",
                    "professional": {
                        "experience": professional.experience if professional else None,
                    } if professional else None
                })

            return {
                "message": "Completed services retrieved successfully",
                "completed": completed
            }, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return {
                "message": "Failed to retrieve completed services",
                "error": str(e)
            }, 500
        

class OngoingServices(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user:
                return {"message": "User not found"}, 404
            if user.role != 'customer':
                return {"message": "Access denied"}, 403

            service_requests = ServiceRequest.query.filter_by(
                customer_id=user_id,
                service_status='accepted'
            ).order_by(ServiceRequest.date_of_request.desc()).all()

            services = []
            for request in service_requests:
                professional = None
                if request.professional_id:
                    user = User.query.get(request.professional_id)
                    professional = Professional.query.filter_by(id=request.professional_id).first()
                    
                services.append({
                    "id": request.id,
                    "serviceName": request.service_type,
                    "professionalName": user.username if user else "Not Assigned",
                    "phoneNo": user.phone if user else "N/A",
                    "bookingDate": request.booking_date.strftime('%Y-%m-%d'),
                    "bookingTime": request.booking_time.strftime('%H:%M'),
                    "status": request.service_status.capitalize(),
                    "professional": {
                        "experience": professional.experience if professional else None,
                    } if professional else None
                })

            return {
                "message": "Ongoing services retrieved successfully",
                "services": services
            }, 200

        except Exception as e:
            db.session.rollback()
            print("Error:", e)
            return {
                "message": "Failed to retrieve ongoing services",
                "error": str(e)
            }, 500

class CustomerFeedbackApproval(Resource):
    @jwt_required()
    def post(self, request_id):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            print(user)
            if not user:
                return {"message": "User not found"}, 404
            if user.role != 'customer':
                return {"message": "Access denied"}, 403

            parser = reqparse.RequestParser()
            parser.add_argument('rating', type=float, required=True, help='Rating is required')
            parser.add_argument('feedback', type=str, required=True, help='Feedback is required')
            data = parser.parse_args()

            service_request = ServiceRequest.query.get(request_id)
            if not service_request:
                return {"message": "Service request not found"}, 404

            if service_request.customer_id != user_id:
                return {"message": "Unauthorized to modify this request"}, 403

            if service_request.service_status != 'accepted':
                return {"message": "Can only complete accepted services"}, 400

            try:
                # Update service request with rating and feedback
                service_request.service_status = 'completed'
                service_request.rating = data['rating']
                service_request.feedback = data['feedback']
                
                # Update professional's average rating
                if service_request.professional_id:
                    professional = Professional.query.get(service_request.professional_id)
                    if professional:
                        completed_services = ServiceRequest.query.filter_by(
                            professional_id=professional.id,
                            service_status='completed'
                        ).all()
                        
                        rated_services = [s for s in completed_services if s.rating is not None]
                        if rated_services:
                            total_rating = sum(s.rating for s in rated_services)
                            professional.rating = total_rating / len(rated_services)
                            professional.rating_count = len(rated_services)

                db.session.commit()
                
                return {
                    "message": "Service completed and feedback submitted successfully",
                    "service_id": request_id,
                    "rating": data['rating'],
                    "feedback": data['feedback']
                }, 200

            except Exception as e:
                db.session.rollback()
                print("Error:", e)
                return {
                    "message": "Failed to submit feedback",
                    "error": str(e)
                }, 500

        except Exception as e:
            print("Error:", e)
            return {
                "message": "Failed to process feedback",
                "error": str(e)
            }, 500