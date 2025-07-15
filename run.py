import os
from app import create_app, db
from app.models import User, PG, Booking, Review, Contact

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'PG': PG,
        'Booking': Booking,
        'Review': Review,
        'Contact': Contact
    }

@app.before_first_request
def create_tables():
    db.create_all()

    # Create default admin user if it doesn't exist
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@pgfinder.com',
            full_name='System Administrator',
            phone='1234567890',
            user_type='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: admin/admin123")

if __name__ == '__main__':
    app.run(debug=True)
