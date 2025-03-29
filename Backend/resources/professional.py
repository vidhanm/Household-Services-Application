from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, ServiceRequest, Professional
from models import db

class ProfessionalDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'professional':
            return {"message": "Access denied"}, 403

        professional = Professional.query.filter_by(user_id=user_id).first()
        if not professional:
            return {"message": "Professional profile not found"}, 404
    
        # Get all service requests that match this professional's service type
        service_requests = ServiceRequest.query.filter(
            (ServiceRequest.service_type == professional.assigned_service) &
            ((ServiceRequest.professional_id == None) | 
             (ServiceRequest.professional_id == professional.id))
        ).all()
    
        return {
            "pending_requests": [
                {
                    "id": sr.id,
                    "service_id": sr.id,
                    "customer_id": sr.customer_id,
                    "date_of_request": sr.date_of_request.isoformat(),
                    "status": sr.service_status,
                    "service_type": sr.service_type,
                    "price": sr.price
                } for sr in service_requests if sr.service_status == 'requested'
            ],
            "accepted_requests": [
                {
                    "id": sr.id,
                    "service_id": sr.id,
                    "customer_id": sr.customer_id,
                    "date_of_request": sr.date_of_request.isoformat(),
                    "status": sr.service_status,
                    "service_type": sr.service_type,
                    "price": sr.price
                } for sr in service_requests if sr.service_status == 'accepted'
            ],
            "rejected_requests": [
                {
                    "id": sr.id,
                    "service_id": sr.id,
                    "customer_id": sr.customer_id,
                    "date_of_request": sr.date_of_request.isoformat(),
                    "status": sr.service_status,
                    "service_type": sr.service_type,
                    "price": sr.price
                } for sr in service_requests if sr.service_status == 'rejected'
            ]
        }

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'professional':
            return {"message": "Access denied"}, 403

        parser = reqparse.RequestParser()
        parser.add_argument('request_id', type=int, required=True)
        parser.add_argument('action', type=str, required=True)
        data = parser.parse_args()

        service_request = ServiceRequest.query.get(data['request_id'])
        if not service_request:
            return {"message": "Service request not found"}, 404

        professional = Professional.query.filter_by(user_id=user_id).first()
        if not professional:
            return {"message": "Professional profile not found"}, 404

        if data['action'] == 'accept':
            service_request.service_status = 'accepted'
            service_request.professional_id = professional.id
        elif data['action'] == 'reject':
            service_request.service_status = 'rejected'
            service_request.professional_id = professional.id  # Set the professional_id here too
        else:
            return {"message": "Invalid action"}, 400

        db.session.commit()

        return {"message": f"Service request {data['action']}ed successfully"}
