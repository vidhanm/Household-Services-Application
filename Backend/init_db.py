from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def init_db():
    with app.app_context():
        db.create_all()

        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', 
                         password=generate_password_hash('admin_password'),
                         role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    init_db()