# CareLink - Digital Care Marketplace

CareLink is a full-stack web application designed to be a digital marketplace connecting people in need of in-home services (Customers) with verified professionals (Providers).

## Features

### Public Pages
- **Home Page**: Clean, professional landing page with hero section and service overview
- **Login Page**: Simple authentication form with role-based redirection
- **Sign Up Page**: Account creation with Customer/Provider role selection

### Customer Features
- **Customer Dashboard**: Personalized homepage with upcoming bookings and quick actions
- **Search/Find Professionals**: Browse and filter verified care providers
- **Professional Profile**: Detailed provider information with interactive booking calendar
- **Booking Process**: Multi-step booking flow with real-time cost calculation
- **Booking History**: View and manage all past and upcoming bookings

### Provider Features
- **Provider Dashboard**: Professional hub with earnings summary and upcoming jobs
- **Profile Management**: Edit professional information with real-time validation
- **Calendar Management**: Set availability and manage schedule
- **Booking Management**: Accept/decline bookings and track service history

## Technology Stack

- **Backend**: Django 4.2.7 with SQLite database
- **Frontend**: HTML, CSS, Tailwind CSS, JavaScript
- **Authentication**: Role-based access control (Customer/Provider)
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CareLinkWeb
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000`
   - Admin panel: `http://127.0.0.1:8000/admin`

## Project Structure

```
CareLinkWeb/
├── carelink/                 # Django project settings
├── accounts/                 # User authentication and profiles
├── services/                 # Service categories and provider services
├── bookings/                 # Booking management and availability
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── home.html            # Landing page
│   ├── login.html           # Login page
│   ├── signup.html          # Registration page
│   ├── customer/            # Customer-specific templates
│   └── provider/              # Provider-specific templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User uploads (profile pictures)
├── requirements.txt          # Python dependencies
└── manage.py               # Django management script
```

## Key Features Implemented

### Role-Based Access Control
- Strict separation between Customer and Provider interfaces
- Role-based URL routing and template rendering
- Secure authentication with automatic redirection

### Interactive User Experience
- Real-time form validation with JavaScript
- Dynamic calendar and time slot selection
- AJAX-powered availability checking
- Responsive design for all device sizes

### Professional Features
- Provider verification system with background checks
- Earnings tracking and performance metrics
- Availability management with calendar integration
- Service management and pricing controls

### Customer Features
- Advanced search and filtering capabilities
- Interactive booking process with cost calculation
- Booking history with status tracking
- Profile management with preferences

## Database Models

- **User**: Extended Django user model with role selection
- **Customer**: Customer-specific profile information
- **Provider**: Professional profile with verification status
- **Service**: Provider services with categories and pricing
- **Booking**: Service bookings with status tracking
- **Availability**: Provider schedule management

## Security Features

- CSRF protection on all forms
- Secure file upload handling
- Input validation and sanitization
- Role-based access control
- Secure authentication system

## Deployment Notes

For production deployment:

1. Set `DEBUG=False` in settings
2. Use a production database (PostgreSQL recommended)
3. Configure static file serving
4. Set up proper media file handling
5. Use environment variables for sensitive data
6. Enable HTTPS
7. Configure proper CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure you have proper licensing for any production use.
