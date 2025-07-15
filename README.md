# PG Finder - Final Year Project

A comprehensive web application for finding and managing Paying Guest (PG) accommodations built with Flask and Python.

## Features

### For Students:
- **User Registration & Authentication** - Secure login system with JWT tokens
- **Advanced Search** - Search PGs by location, price, amenities, and more
- **PG Details** - View comprehensive information about each PG including photos, facilities, and reviews
- **Booking System** - Book PGs directly through the platform
- **Review System** - Rate and review PGs based on experience
- **User Dashboard** - Manage bookings and profile information
- **Responsive Design** - Works seamlessly on desktop and mobile devices

### For PG Owners:
- **PG Management** - Add, edit, and manage PG listings
- **Booking Management** - View and manage booking requests
- **Analytics Dashboard** - Track bookings and performance metrics
- **Photo Gallery** - Upload multiple photos for each PG
- **Contact Management** - Manage communication with potential tenants

### For Administrators:
- **User Management** - Manage users and PG owners
- **Content Moderation** - Review and approve PG listings
- **Analytics** - System-wide analytics and reporting
- **Support System** - Handle user queries and complaints

## Technology Stack

### Backend:
- **Python 3.8+** - Core programming language
- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling and validation
- **Werkzeug** - Password hashing and security
- **PyJWT** - JWT token authentication
- **SQLite/PostgreSQL** - Database

### Frontend:
- **HTML5** - Markup language
- **CSS3** - Styling and layout
- **Bootstrap 4** - Responsive UI framework
- **JavaScript** - Client-side interactivity
- **jQuery** - DOM manipulation
- **Font Awesome** - Icons

### Deployment:
- **Gunicorn** - WSGI server
- **Heroku** - Cloud platform
- **PostgreSQL** - Production database

## Installation and Setup

### Prerequisites:
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/pg-finder.git
cd pg-finder
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Environment Variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database.db
FLASK_ENV=development
```

### Step 5: Initialize Database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Step 6: Run the Application
```bash
python run.py
```

Visit `http://localhost:5000` in your browser.

## Default Login Credentials

- **Admin**: username: `admin`, password: `admin123`

## Project Structure

```
pg_finder_project/
├── app/
│   ├── __init__.py          # Application factory
│   ├── models.py            # Database models
│   ├── views.py             # Main route handlers
│   ├── auth.py              # Authentication routes
│   ├── forms.py             # WTForms form classes
│   ├── utils.py             # Utility functions
│   └── config.py            # Configuration settings
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── img/
├── migrations/              # Database migrations
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── .env                     # Environment variables
└── README.md               # This file
```

## Database Schema

### Users Table
- User authentication and profile information
- Different user types (student, pg_owner, admin)
- Password hashing for security

### PGs Table
- PG listing information
- Location and pricing details
- Facilities and amenities
- Contact information

### Bookings Table
- Booking requests and status
- Move-in dates and notes
- User-PG relationship

### Reviews Table
- User reviews and ratings
- Comment system for feedback

## API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### PG Management
- `GET /api/pgs` - Get all PGs (JSON API)
- `GET /pg/<id>` - Get specific PG details
- `POST /add_pg` - Add new PG (PG owners only)
- `POST /book_pg/<id>` - Book a PG

### User Management
- `GET /profile` - View user profile
- `POST /profile` - Update user profile
- `GET /dashboard` - User dashboard

## Security Features

- **Password Hashing** - Secure password storage using Werkzeug
- **CSRF Protection** - Cross-site request forgery protection
- **SQL Injection Prevention** - SQLAlchemy ORM prevents SQL injection
- **XSS Protection** - Template escaping prevents cross-site scripting
- **Authentication Required** - Protected routes require login
- **Role-Based Access** - Different access levels for different user types

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

## Deployment

### Heroku Deployment

1. Create a Heroku app:
```bash
heroku create pg-finder-app
```

2. Add PostgreSQL addon:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

4. Deploy:
```bash
git push heroku main
```

5. Initialize database:
```bash
heroku run flask db upgrade
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Developer**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [https://github.com/yourusername]
- **LinkedIn**: [https://linkedin.com/in/yourprofile]

## Acknowledgments

- Flask documentation and community
- Bootstrap for responsive design
- SQLAlchemy for database ORM
- All the open-source libraries that made this project possible

## Future Enhancements

- **Real-time Chat** - Integration with WebSocket for real-time messaging
- **Payment Gateway** - Integration with payment processors
- **Mobile App** - React Native or Flutter mobile application
- **Advanced Analytics** - Detailed analytics and reporting
- **Email Notifications** - Automated email notifications
- **Social Login** - Google, Facebook, LinkedIn login integration
- **Multi-language Support** - Internationalization (i18n)
- **Advanced Search** - Elasticsearch integration for better search
- **Map Integration** - Google Maps API for location services
- **Photo Upload** - Cloud storage for images (AWS S3, Cloudinary)
