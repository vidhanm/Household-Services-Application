from config import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        from models import User, Service, Professional, ServiceRequest
        db.create_all()
    app.run(debug=True)