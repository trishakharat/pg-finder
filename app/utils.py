import os
import secrets
from PIL import Image
from flask import current_app

def save_picture(form_picture):
    """Save uploaded picture and return filename"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)

    # Create uploads directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    # Resize image
    output_size = (800, 600)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:,.0f}"

def format_date(date):
    """Format date for display"""
    return date.strftime('%B %d, %Y')

def get_pg_type_label(pg_type):
    """Get display label for PG type"""
    labels = {
        'boys': 'Boys Only',
        'girls': 'Girls Only',
        'co-ed': 'Co-ed'
    }
    return labels.get(pg_type, pg_type)

def get_room_type_label(room_type):
    """Get display label for room type"""
    labels = {
        'single': 'Single Occupancy',
        'double': 'Double Sharing',
        'triple': 'Triple Sharing',
        'sharing': 'Multiple Sharing'
    }
    return labels.get(room_type, room_type)

def get_booking_status_label(status):
    """Get display label for booking status"""
    labels = {
        'pending': 'Pending',
        'confirmed': 'Confirmed',
        'cancelled': 'Cancelled',
        'completed': 'Completed'
    }
    return labels.get(status, status)

def get_star_rating_html(rating):
    """Get HTML for star rating display"""
    stars = ''
    for i in range(5):
        if i < rating:
            stars += '<i class="fas fa-star text-warning"></i>'
        else:
            stars += '<i class="far fa-star text-muted"></i>'
    return stars

def paginate_query(query, page, per_page=10):
    """Paginate a query"""
    return query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def send_email(to, subject, template, **kwargs):
    """Send email (placeholder function)"""
    # This would be implemented with Flask-Mail
    # For now, just log the email
    print(f"Sending email to {to}: {subject}")
    print(f"Template: {template}")
    print(f"Data: {kwargs}")
    return True
