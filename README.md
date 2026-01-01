# 🗑️💰 TRASH2CASH - Smart Waste Management System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.1+-green.svg)](https://www.djangoproject.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**TRASH2CASH** is an intelligent IoT-based waste management system that rewards users for proper waste disposal. The system uses AI-powered waste classification, QR-code based user identification, and a points-based reward system to encourage sustainable waste management practices.

## 🌟 Key Features

### 🤖 AI-Powered Waste Classification

- Real-time waste detection and classification using TensorFlow/Keras
- Automated compartment selection (Recyclable, Non-Recyclable, Organic)
- Computer vision with OpenCV for image processing

### 📱 QR Code Authentication

- Secure user identification via QR code scanning
- Mobile app integration ready
- Session-based disposal tracking

### 🎁 Rewards & Gamification

- Points system for waste disposal
- Redeemable rewards catalog
- User leaderboards and achievements
- Real-time point tracking

### 🗺️ Smart Bin Locator

- Interactive map using Leaflet.js (Free - No API costs!)
- Find nearby bins with capacity status
- One-tap navigation to bin locations
- Real-time bin fill level monitoring

### 📊 Admin Dashboard

- Real-time monitoring of all smart bins
- Waste disposal analytics
- User management and reward redemption approval
- Issue reporting and tracking system

### 🔔 Notifications System

- Real-time alerts for disposal confirmations
- Reward redemption updates
- Bin maintenance notifications

## 🛠️ Tech Stack

### Backend

- **Framework:** Django 5.1+
- **Database:** SQLite3 (Development) / PostgreSQL (Production Ready)
- **AI/ML:** TensorFlow 2.15+, Keras 3.0+
- **Computer Vision:** OpenCV, Pillow
- **QR Processing:** pyzbar

### Frontend

- **Templates:** Django Templates
- **CSS Framework:** Bootstrap 5.3.7
- **Maps:** Leaflet.js (Free alternative to Google Maps)
- **JavaScript:** Vanilla JS with AJAX

### IoT Hardware

- **Microcontroller:** ESP32-CAM
- **Sensors:** Ultrasonic (HC-SR04), Load Cells
- **Camera:** ESP32 Built-in Camera Module
- **Actuators:** Servo Motors for compartment control

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Afshan-Farooq-dev/Trash2cash.git
   cd Trash2cash
   ```

2. **Create virtual environment**

   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**

   - Windows:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Configuration**

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your configuration
   # (SECRET_KEY, DEBUG, etc.)
   ```

6. **Run migrations**

   ```bash
   python manage.py migrate
   ```

7. **Create superuser (Admin)**

   ```bash
   python manage.py createsuperuser
   ```

8. **Create test bins (Optional)**

   ```bash
   python create_lahore_bins.py
   ```

9. **Run the development server**

   ```bash
   python manage.py runserver
   ```

10. **Access the application**
    - User Interface: http://127.0.0.1:8000/
    - Admin Panel: http://127.0.0.1:8000/admin/

## 🚀 Quick Start Scripts

### Windows PowerShell

```powershell
# Quick setup and run
.\quickstart.ps1

# Run server only
.\run.ps1
```

## 📁 Project Structure

```
Trash2cash/
├── Light/                      # Main Django app
│   ├── models.py              # Database models
│   ├── views.py               # Core views & AI processing
│   ├── user_views.py          # User-facing views
│   ├── admin_views.py         # Admin dashboard views
│   ├── mobile_api.py          # Mobile app API endpoints
│   ├── qr_disposal_api.py     # QR-based disposal API
│   ├── templates/             # HTML templates
│   ├── static/                # CSS, JS, images
│   └── migrations/            # Database migrations
├── Traffic/                   # Django project settings
│   ├── settings.py           # Project configuration
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI configuration
├── media/                     # User uploads (gitignored)
├── archive_docs/             # Project documentation
├── scripts/                  # Utility scripts
├── esp32_waste_bin.ino      # Arduino code for ESP32
├── waste_classifier_final.keras  # AI model (gitignored)
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
└── README.md                 # This file
```

## 🎮 Usage

### For Users

1. **Register/Login** - Create account with CNIC verification
2. **Find Bins** - Use the interactive map to locate nearby smart bins
3. **Dispose Waste** - Scan your QR code at the bin, place waste in front of camera
4. **Earn Points** - Get points automatically based on waste type
5. **Redeem Rewards** - Exchange points for real rewards in the store

### For Admins

1. **Login to Admin Panel** - `/admin/`
2. **Monitor Bins** - Real-time bin status and fill levels
3. **Manage Users** - View user profiles and transaction history
4. **Approve Redemptions** - Process reward redemption requests
5. **View Analytics** - Track waste disposal trends and statistics

## 🔌 API Endpoints

### Mobile API

```
POST   /api/mobile/register/          # User registration
POST   /api/mobile/login/             # User authentication
GET    /api/mobile/profile/           # Get user profile
GET    /api/mobile/bins/nearby/       # Get nearby bins
POST   /api/mobile/dispose/           # Record waste disposal
GET    /api/mobile/rewards/           # Get available rewards
POST   /api/mobile/redeem/            # Redeem reward
```

### QR Disposal API

```
POST   /api/qr-disposal/scan/         # Scan QR and start session
POST   /api/qr-disposal/classify/     # Classify waste
POST   /api/qr-disposal/complete/     # Complete disposal
```

## 🔐 Security Features

- ✅ API keys stored in environment variables (not in repository)
- ✅ CNIC validation for user registration
- ✅ Session-based authentication
- ✅ SQL injection protection (Django ORM)
- ✅ CSRF protection enabled
- ✅ Password hashing with Django's authentication system

## 📊 Database Models

- **User** - Django built-in user model
- **UserProfile** - Extended user information with CNIC, QR code, points
- **Bin** - Smart bin locations and status
- **WasteRecord** - Disposal transaction history
- **RewardItem** - Available rewards catalog
- **RewardRedemption** - User redemption history
- **IssueReport** - User-reported bin issues
- **Notification** - User notification system

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 System Architecture

For detailed technical information about the system design, data flow, and implementation details, see:

**[📖 ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture and technical documentation

## 🐛 Known Issues

- ML model files (`.h5`, `.keras`) are large and not included in repository
- Database file (`db.sqlite3`) is excluded for security - needs fresh setup
- Test files are excluded from production deployment

## 📧 Contact

**Project Maintainer:** Afshan Farooq

- GitHub: [@Afshan-Farooq-dev](https://github.com/Afshan-Farooq-dev)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- TensorFlow team for AI/ML framework
- Django community for the robust web framework
- Leaflet.js for free mapping solution
- Bootstrap for UI components

---

**Made with ❤️ for a cleaner, greener future 🌍♻️**
