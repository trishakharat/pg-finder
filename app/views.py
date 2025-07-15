from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from app import db
from app.models import PG, User, Booking, Review, Contact
from app.forms import PGForm, SearchForm, BookingForm, ReviewForm, ContactForm, ProfileForm
from app.utils import save_picture

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get recent PGs for homepage
    recent_pgs = PG.query.filter_by(is_active=True).order_by(PG.created_at.desc()).limit(6).all()

    # Get cities for search dropdown
    cities = db.session.query(PG.city).distinct().all()
    cities = [city[0] for city in cities]

    return render_template('index.html', pgs=recent_pgs, cities=cities)

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'pg_owner':
        # PG Owner dashboard
        pgs = PG.query.filter_by(owner_id=current_user.id).all()
        total_pgs = len(pgs)
        total_bookings = Booking.query.join(PG).filter(PG.owner_id == current_user.id).count()
        pending_bookings = Booking.query.join(PG).filter(
            and_(PG.owner_id == current_user.id, Booking.status == 'pending')
        ).count()

        return render_template('dashboard.html', 
                             pgs=pgs, 
                             total_pgs=total_pgs, 
                             total_bookings=total_bookings, 
                             pending_bookings=pending_bookings)
    else:
        # Student dashboard
        bookings = Booking.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', bookings=bookings)

@main.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    pgs = []

    if form.validate_on_submit():
        query = PG.query.filter_by(is_active=True)

        if form.city.data:
            query = query.filter(PG.city.contains(form.city.data))

        if form.pg_type.data:
            query = query.filter(PG.pg_type == form.pg_type.data)

        if form.room_type.data:
            query = query.filter(PG.room_type == form.room_type.data)

        if form.min_rent.data:
            query = query.filter(PG.rent_amount >= form.min_rent.data)

        if form.max_rent.data:
            query = query.filter(PG.rent_amount <= form.max_rent.data)

        if form.facilities.data:
            facility_map = {
                'wifi': PG.wifi,
                'parking': PG.parking,
                'meals': PG.meals,
                'ac': PG.ac
            }
            if form.facilities.data in facility_map:
                query = query.filter(facility_map[form.facilities.data] == True)

        pgs = query.order_by(PG.created_at.desc()).all()

    return render_template('search_results.html', form=form, pgs=pgs)

@main.route('/pg/<int:id>')
def pg_detail(id):
    pg = PG.query.get_or_404(id)
    reviews = Review.query.filter_by(pg_id=id).order_by(Review.created_at.desc()).all()

    # Check if user has already reviewed this PG
    user_reviewed = False
    if current_user.is_authenticated:
        user_reviewed = Review.query.filter_by(user_id=current_user.id, pg_id=id).first() is not None

    return render_template('pg_detail.html', pg=pg, reviews=reviews, user_reviewed=user_reviewed)

@main.route('/add_pg', methods=['GET', 'POST'])
@login_required
def add_pg():
    if current_user.user_type != 'pg_owner':
        flash('Only PG owners can add PGs.', 'warning')
        return redirect(url_for('main.index'))

    form = PGForm()
    if form.validate_on_submit():
        pg = PG(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            pincode=form.pincode.data,
            rent_amount=form.rent_amount.data,
            deposit_amount=form.deposit_amount.data,
            pg_type=form.pg_type.data,
            room_type=form.room_type.data,
            total_rooms=form.total_rooms.data,
            available_rooms=form.available_rooms.data,
            wifi=form.wifi.data,
            parking=form.parking.data,
            laundry=form.laundry.data,
            meals=form.meals.data,
            ac=form.ac.data,
            gym=form.gym.data,
            security=form.security.data,
            power_backup=form.power_backup.data,
            contact_person=form.contact_person.data,
            contact_phone=form.contact_phone.data,
            contact_email=form.contact_email.data,
            owner_id=current_user.id
        )
        db.session.add(pg)
        db.session.commit()
        flash('PG added successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_pg.html', form=form)

@main.route('/book_pg/<int:id>', methods=['GET', 'POST'])
@login_required
def book_pg(id):
    if current_user.user_type != 'student':
        flash('Only students can book PGs.', 'warning')
        return redirect(url_for('main.pg_detail', id=id))

    pg = PG.query.get_or_404(id)

    # Check if user has already booked this PG
    existing_booking = Booking.query.filter_by(user_id=current_user.id, pg_id=id).first()
    if existing_booking:
        flash('You have already booked this PG.', 'warning')
        return redirect(url_for('main.pg_detail', id=id))

    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(
            user_id=current_user.id,
            pg_id=id,
            move_in_date=form.move_in_date.data,
            notes=form.notes.data
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking request submitted successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('book_pg.html', form=form, pg=pg)

@main.route('/add_review/<int:id>', methods=['POST'])
@login_required
def add_review(id):
    if current_user.user_type != 'student':
        flash('Only students can add reviews.', 'warning')
        return redirect(url_for('main.pg_detail', id=id))

    # Check if user has already reviewed this PG
    existing_review = Review.query.filter_by(user_id=current_user.id, pg_id=id).first()
    if existing_review:
        flash('You have already reviewed this PG.', 'warning')
        return redirect(url_for('main.pg_detail', id=id))

    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            pg_id=id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added successfully!', 'success')

    return redirect(url_for('main.pg_detail', id=id))

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(current_user.email)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        form.phone.data = current_user.phone

    return render_template('user_profile.html', form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash('Message sent successfully! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))

    return render_template('contact.html', form=form)

@main.route('/api/pgs')
def api_pgs():
    # Simple API endpoint to get PGs data
    pgs = PG.query.filter_by(is_active=True).all()
    pg_list = []

    for pg in pgs:
        pg_data = {
            'id': pg.id,
            'name': pg.name,
            'city': pg.city,
            'rent_amount': pg.rent_amount,
            'pg_type': pg.pg_type,
            'room_type': pg.room_type,
            'available_rooms': pg.available_rooms,
            'rating': pg.get_average_rating(),
            'facilities': pg.get_facilities()
        }
        pg_list.append(pg_data)

    return jsonify(pg_list)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/terms')
def terms():
    return render_template('terms.html')
