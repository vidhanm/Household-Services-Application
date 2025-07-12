import csv
import os
from datetime import datetime, timedelta, timezone
from flask import current_app
from config import celery
from utils.mail_setup import send_daily_mail, send_monthly_activity_report
from models import db, ServiceRequest, User, Service, Professional

@celery.task
def send_daily_professional_reminders():
    """
    Daily task to send reminders to professionals with pending service requests.
    """
    try:
        # Find service requests with status 'accepted'
        pending_requests = ServiceRequest.query.filter_by(service_status='accepted').all()
        sent_count = 0
        
        for request in pending_requests:
            # Check if professional exists and has pending requests
            if request.professional_id:
                professional = Professional.query.get(request.professional_id)
                if professional and professional.email:
                    # Get user associated with professional
                    user = User.query.get(professional.user_id)
                    if user:
                        # Get service details
                        service_name = request.service_type
                        
                        # Send email reminder
                        send_daily_mail(
                            email=professional.email, 
                            p_name=user.username, 
                            service_name=service_name,
                            request_date=request.date_of_request
                        )
                        sent_count += 1
        
        return f"Successfully sent {sent_count} reminders to professionals"
    except Exception as e:
        print(f"Error in send_daily_professional_reminders: {e}")
        return f"Error sending reminders: {str(e)}"


@celery.task
def send_monthly_activity_report_to_users():
    """
    Monthly task to send activity reports to all users.
    """
    try:
        # Find all users with role='customer'
        users = User.query.filter_by(role='customer').all()
        sent_count = 0
        
        # Get statistics
        total_services = Service.query.count()
        total_completed_requests = ServiceRequest.query.filter_by(service_status='completed').count()
        total_pending_requests = ServiceRequest.query.filter_by(service_status='requested').count()
        
        # Calculate average rating
        completed_with_ratings = ServiceRequest.query.filter(
            ServiceRequest.service_status == 'completed',
            ServiceRequest.rating.isnot(None)
        ).all()
        
        avg_rating = 0
        if completed_with_ratings:
            total_rating = sum(float(request.rating) for request in completed_with_ratings if request.rating)
            avg_rating = total_rating / len(completed_with_ratings) if completed_with_ratings else 0
        
        # Previous month date range
        today = datetime.now()
        first_day_of_month = datetime(today.year, today.month, 1)
        last_month_end = first_day_of_month - timedelta(days=1)
        last_month_start = datetime(last_month_end.year, last_month_end.month, 1)
        
        # Report period string
        report_period = f"{last_month_start.strftime('%B %Y')}"
        
        for user in users:
            if user.email:
                try:
                    # Get user's specific statistics
                    user_completed_requests = ServiceRequest.query.filter_by(
                        customer_id=user.id,
                        service_status='completed'
                    ).count()
                    
                    user_pending_requests = ServiceRequest.query.filter_by(
                        customer_id=user.id,
                        service_status='requested'
                    ).count()
                    
                    # Send mail with statistics
                    send_monthly_activity_report(
                        email=user.email,
                        user_name=user.username,
                        report_period=report_period,
                        total_services=total_services,
                        total_completed=total_completed_requests,
                        total_pending=total_pending_requests,
                        avg_rating=avg_rating,
                        user_completed=user_completed_requests,
                        user_pending=user_pending_requests
                    )
                    
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending report to {user.email}: {e}")
        
        return f"Sent {sent_count} monthly reports out of {len(users)} users"
    except Exception as e:
        print(f"Error in send_monthly_activity_report_to_users: {e}")
        return f"Error sending monthly reports: {str(e)}"


@celery.task
def export_service_requests_to_csv(admin_email):
    """
    Export all completed service requests to CSV and email to admin.
    """
    try:
        print("Exporting service requests to CSV...")
        # Get completed service requests
        completed_requests = ServiceRequest.query.filter_by(service_status='completed').all()
        
        if not completed_requests:
            print("No completed service requests found")
            # Send email notification even when no requests found
            send_monthly_activity_report(
                email=admin_email, 
                user_name="Admin",
                report_period=datetime.now().strftime('%B %Y'),
                message="No completed service requests found to export."
            )
            return "No completed service requests to export"
        
        # Generate unique filename
        filename = f'service_requests_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        export_folder = current_app.config.get('EXPORT_FOLDER', '/tmp')
        try:
            os.makedirs(export_folder, exist_ok=True)
            print(f"Export folder ensured: {export_folder}")
        except Exception as e:
            print(f"Error creating export folder: {e}")
            # Use a fallback location if needed
            export_folder = '/tmp'
        filepath = os.path.join(export_folder, filename)
        print(f"Creating CSV at: {filepath}")
        
        # Create CSV
        with open(filepath, 'w', newline='') as csvfile:
            fieldnames = [
                'id', 'customer_id', 'professional_id', 
                'service_type', 'price', 'booking_date',
                'booking_time', 'duration', 'service_status',
                'date_of_request', 'rating', 'feedback'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for request in completed_requests:
                writer.writerow({
                    'id': request.id,
                    'customer_id': request.customer_id,
                    'professional_id': request.professional_id,
                    'service_type': request.service_type,
                    'price': request.price,
                    'booking_date': request.booking_date.strftime('%Y-%m-%d') if request.booking_date else '',
                    'booking_time': request.booking_time.strftime('%H:%M') if request.booking_time else '',
                    'duration': request.duration,
                    'service_status': request.service_status,
                    'date_of_request': request.date_of_request.strftime('%Y-%m-%d %H:%M:%S') if request.date_of_request else '',
                    'rating': request.rating if request.rating else '',
                    'feedback': request.feedback if request.feedback else ''
                })
        
        print(f"CSV file created with {len(completed_requests)} records")
        
        # Send email with CSV attachment
        send_monthly_activity_report(
            email=admin_email, 
            filename=filename, 
            filepath=filepath
        )
        
        # Cleanup file after sending
        try:
            os.remove(filepath)
            print(f"Temporary CSV file removed: {filepath}")
        except Exception as e:
            print(f"Warning: Could not remove temporary file {filepath}: {e}")
        
        return f"Exported {len(completed_requests)} service requests to {admin_email}"
    except Exception as e:
        print(f"Error in export_service_requests_to_csv: {e}")
        return f"Error exporting service requests: {str(e)}"


@celery.task
def cleanup_old_exports():
    """
    Clean up export files older than 3 days
    """
    try:
        export_folder = current_app.config.get('EXPORT_FOLDER', '/tmp')
        if not os.path.exists(export_folder):
            return "Export folder does not exist"
        
        cutoff_time = datetime.now() - timedelta(days=3)
        deleted_count = 0
        
        for filename in os.listdir(export_folder):
            if filename.startswith('service_requests_'):
                file_path = os.path.join(export_folder, filename)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                if file_modified < cutoff_time:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting old export {file_path}: {e}")
        
        return f"Cleaned up {deleted_count} old export files"
    except Exception as e:
        print(f"Error in cleanup_old_exports: {e}")
        return f"Error cleaning up old exports: {str(e)}"


@celery.task
def update_service_statistics():
    """
    Update service statistics (ratings) for all services
    """
    try:
        # Get all services
        services = Service.query.all()
        updated_count = 0
        
        for service in services:
            # Find service requests for this service type that have ratings
            service_requests = ServiceRequest.query.filter(
                ServiceRequest.service_type == service.name,
                ServiceRequest.rating.isnot(None),
                ServiceRequest.service_status == 'completed'
            ).all()
            
            # Calculate new average rating
            if service_requests:
                total_rating = sum(float(req.rating) for req in service_requests if req.rating)
                avg_rating = total_rating / len(service_requests)
                rating_count = len(service_requests)
                
                # Update service rating
                service.rating = avg_rating
                service.rating_count = rating_count
                updated_count += 1
        
        # Commit changes to database
        db.session.commit()
        
        return f"Updated statistics for {updated_count} services"
    except Exception as e:
        db.session.rollback()
        print(f"Error in update_service_statistics: {e}")
        return f"Error updating service statistics: {str(e)}"