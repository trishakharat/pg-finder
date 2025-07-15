from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='student')  # student, pg_owner, admin
    profile_pic = db.Column(db.String(200), default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    pgs = db.relationship('PG', backref='owner', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class PG(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    rent_amount = db.Column(db.Float, nullable=False)
    deposit_amount = db.Column(db.Float, nullable=False)
    pg_type = db.Column(db.String(20), nullable=False)  # boys, girls, co-ed
    room_type = db.Column(db.String(20), nullable=False)  # single, double, triple, sharing
    total_rooms = db.Column(db.Integer, nullable=False)
    available_rooms = db.Column(db.Integer, nullable=False)

    # Facilities
    wifi = db.Column(db.Boolean, default=False)
    parking = db.Column(db.Boolean, default=False)
    laundry = db.Column(db.Boolean, default=False)
    meals = db.Column(db.Boolean, default=False)
    ac = db.Column(db.Boolean, default=False)
    gym = db.Column(db.Boolean, default=False)
    security = db.Column(db.Boolean, default=False)
    power_backup = db.Column(db.Boolean, default=False)

    # Contact
    contact_person = db.Column(db.String(100), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    contact_email = db.Column(db.String(120), nullable=True)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    # Foreign Keys
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    images = db.relationship('PGImage', backref='pg', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='pg', lazy=True)
    reviews = db.relationship('Review', backref='pg', lazy=True)

    def __repr__(self):
        return f'<PG {self.name}>'

    def get_average_rating(self):
        reviews = Review.query.filter_by(pg_id=self.id).all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / len(reviews)

    def get_facilities(self):
        facilities = []
        if self.wifi: facilities.append('WiFi')
        if self.parking: facilities.append('Parking')
        if self.laundry: facilities.append('Laundry')
        if self.meals: facilities.append('Meals')
        if self.ac: facilities.append('AC')
        if self.gym: facilities.append('Gym')
        if self.security: facilities.append('Security')
        if self.power_backup: facilities.append('Power Backup')
        return facilities

class PGImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    pg_id = db.Column(db.Integer, db.ForeignKey('pg.id'), nullable=False)

    def __repr__(self):
        return f'<PGImage {self.filename}>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    move_in_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, cancelled, completed
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg.id'), nullable=False)

    def __repr__(self):
        return f'<Booking {self.id}>'

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pg_id = db.Column(db.Integer, db.ForeignKey('pg.id'), nullable=False)

    def __repr__(self):
        return f'<Review {self.id}>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_responded = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Contact {self.name}>'
