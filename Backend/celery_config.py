from celery import Celery
import os

def init_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['task']
    )
    celery.conf.update(
        broker_transport_options={
            'visibility_timeout': 3600,
            'polling_interval': 10.0,
        },
        worker_prefetch_multiplier=1,
        task_acks_late=True,
        broker_connection_retry_on_startup=True,
        redis_host=os.environ.get('REDIS_HOST', 'redis'),
        redis_port=int(os.environ.get('REDIS_PORT', 6379))
    )

    celery.conf.beat_schedule = {
        'send-daily-professional-reminders': {
            'task': 'task.send_daily_professional_reminders',
            # 'schedule': 60 * 60 * 24,  # Run once every day (in seconds)
            "schedule": 60
        },
        'send-monthly-activity-report': {
            'task': 'task.send_monthly_activity_report_to_users',  # Fixed task name
            'schedule': 60 * 60 * 24 * 30,  # Run once every 30 days (in seconds)
        },
        'update-service-statistics': {  # Added this task to run periodically
            'task': 'task.update_service_statistics',
            'schedule': 60 * 60 * 12,  # Run twice a day (every 12 hours)
        },
        'cleanup-old-exports': {  # Added this task to run periodically
            'task': 'task.cleanup_old_exports',
            'schedule': 60 * 60 * 24,  # Run once a day
        }
    }

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery