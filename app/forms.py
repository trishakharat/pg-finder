from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, IntegerField, BooleanField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from wtforms.widgets import TextArea
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    user_type = SelectField('User Type', choices=[('student', 'Student'), ('pg_owner', 'PG Owner')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')

class PGForm(FlaskForm):
    name = StringField('PG Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10, max=200)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=2, max=50)])
    pincode = StringField('Pincode', validators=[DataRequired(), Length(min=6, max=10)])

    rent_amount = FloatField('Monthly Rent (₹)', validators=[DataRequired(), NumberRange(min=1000, max=100000)])
    deposit_amount = FloatField('Security Deposit (₹)', validators=[DataRequired(), NumberRange(min=0, max=200000)])

    pg_type = SelectField('PG Type', choices=[('boys', 'Boys Only'), ('girls', 'Girls Only'), ('co-ed', 'Co-ed')], validators=[DataRequired()])
    room_type = SelectField('Room Type', choices=[('single', 'Single'), ('double', 'Double'), ('triple', 'Triple'), ('sharing', 'Sharing')], validators=[DataRequired()])

    total_rooms = IntegerField('Total Rooms', validators=[DataRequired(), NumberRange(min=1, max=100)])
    available_rooms = IntegerField('Available Rooms', validators=[DataRequired(), NumberRange(min=0, max=100)])

    # Facilities
    wifi = BooleanField('WiFi')
    parking = BooleanField('Parking')
    laundry = BooleanField('Laundry')
    meals = BooleanField('Meals')
    ac = BooleanField('AC')
    gym = BooleanField('Gym')
    security = BooleanField('Security')
    power_backup = BooleanField('Power Backup')

    # Contact Information
    contact_person = StringField('Contact Person', validators=[DataRequired(), Length(min=2, max=100)])
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(min=10, max=15)])
    contact_email = StringField('Contact Email', validators=[Email()])

    submit = SubmitField('Add PG')

class SearchForm(FlaskForm):
    city = StringField('City', validators=[DataRequired()])
    pg_type = SelectField('PG Type', choices=[('', 'Any'), ('boys', 'Boys Only'), ('girls', 'Girls Only'), ('co-ed', 'Co-ed')])
    room_type = SelectField('Room Type', choices=[('', 'Any'), ('single', 'Single'), ('double', 'Double'), ('triple', 'Triple'), ('sharing', 'Sharing')])
    min_rent = FloatField('Min Rent (₹)', validators=[NumberRange(min=0, max=100000)])
    max_rent = FloatField('Max Rent (₹)', validators=[NumberRange(min=0, max=100000)])
    facilities = SelectField('Facilities', choices=[('', 'Any'), ('wifi', 'WiFi'), ('parking', 'Parking'), ('meals', 'Meals'), ('ac', 'AC')])
    submit = SubmitField('Search')

class BookingForm(FlaskForm):
    move_in_date = DateField('Move-in Date', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes', validators=[Length(max=500)])
    submit = SubmitField('Book PG')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Review', validators=[Length(max=500)])
    submit = SubmitField('Submit Review')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=2, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Update Profile')

    def __init__(self, original_email, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Please use a different email address.')
