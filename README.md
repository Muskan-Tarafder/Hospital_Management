# HMS
An Integrated Hospital Management System with Serverless Notifications & Google Calendar Sync.

Healthcare Management System (HMS) is designed to bridge the gap between doctors and patients. The platform leverages a decoupled architecture, using Django for the core logic and an AWS Lambda-style Serverless microservice for automated communication.

## Key Features
- Role-Based Access Control: Separate, customized dashboards for Doctors and Patients.

-Google Calendar API Integration: Doctors can sync their booked slots directly to their Google Calendar, ensuring they never miss a consultation.

-Serverless Email Microservice: A dedicated Node.js/Python service built with the Serverless Framework that triggers instant email notifications upon booking.

-Real-time Availability: Patients can browse specialized doctors and book real-time slots.

-Modern UI/UX: A professional, responsive interface built with Bootstrap 5 and Crispy Forms.

## Tech Stack

### Backend
Framework: Django (Python 3.x)

Database: PostgreSQL (Production-ready relational storage)

Authentication: Django Auth with Role-based Groups

### Microservices
Framework: Serverless Framework

Environment: AWS Lambda (Simulated via Serverless Offline)

Service: Node.js/Python handler for SMTP communication

### APIs & Tools
Google Calendar API: OAuth2 integration for schedule synchronization.

Gmail SMTP: Secure automated mailing using App Passwords.

Frontend: Bootstrap 5, FontAwesome, Google Fonts.




## Project Structure
```bash
├── hms/                        # Django Project Root
│   ├── hmsApp/                 # Main Application Logic
│   ├── templates/              # Styled HTML UI (Bootstrap 5)
│   └── manage.py
├── hms_email_service/          # Serverless Microservice
│   ├── handler.py              # Email logic (Python)
│   ├── serverless.yml          # Infrastructure as Code (IaC)
│   └── package.json
└── oauth.json                  # Google API Credentials (Hidden)
```


## Installation & Setup

1. Backend Setup
```bash
# Clone the repository
git clone https://github.com/Muskan-Tarafder/Hospital_Management.git

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the Django server
python manage.py runserver
```

2. Email Microservice Setup
```bash
cd hms_email_service

# Install Serverless globally
npm install -g serverless

# Install dependencies
npm install

# Start the service offline
npx serverless offline --noTimeout
```

## System Architecture

Patient books a slot on the Django Web Portal.

Django saves the appointment to PostgreSQL and triggers a POST request to the Serverless API.

Serverless Lambda processes the request and sends a confirmation email to the patient via Gmail SMTP.

Google Calendar API simultaneously creates an event on the Doctor's calendar with a 5.5-hour offset (IST adjustment).

## Author
Muskan Tarafder
