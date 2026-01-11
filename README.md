# CodeHub - Cloud-Based Repository & Python Environment Platform

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create Virtual Environment](#2-create-virtual-environment)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Environment Configuration](#4-environment-configuration)
  - [5. Firebase Setup](#5-firebase-setup)
  - [6. Email Configuration](#6-email-configuration)
  - [7. Database Migrations](#7-database-migrations)
  - [8. Run the Development Server](#8-run-the-development-server)
- [Usage Guide](#usage-guide)
  - [Authentication Workflow](#authentication-workflow)
  - [Repository Management](#repository-management)
  - [File Operations](#file-operations)
  - [Python Code Execution](#python-code-execution)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**CodeHub** is a Django web application that allows users to:

- **Create and manage repositories** (public/private) with version control features
- **Store and organize code files** across multiple repositories
- **Execute Python code** in a sandboxed environment with real-time output capture
- **Visualize matplotlib plots** generated from executed code
- **Reset forgotten passwords** using OTP-based verification
- **Browse public repositories** from other users

The platform uses **Firebase Authentication** for secure user management and **Django** for backend logic, providing a seamless experience for coding, sharing, and collaboration.

---

## Key Features

### 🔐 Authentication & Security
- **Firebase Authentication** for secure user registration and login
- **OTP-based password reset** with email verification
- **Session management** using Django signed cookies
- **Login-required decorators** protecting sensitive views

### 📦 Repository Management
- Create **public and private repositories** with descriptions
- **Ownership-based access control** - users see only their repos and public ones
- **File organization** within repositories with hierarchical structure
- **Timestamp tracking** for created and updated dates

### 🐍 Python Code Execution Environment
- **Real-time Python code execution** via AJAX requests
- **Output capturing** for `print()` statements and standard output
- **Matplotlib integration** for data visualization
- **Interactive input handling** for `input()` function calls
- **Error reporting** with detailed execution error messages
- **Stateless execution** - each run is isolated

### 📝 File Management
- **Create new files** within repositories
- **Edit existing files** with content updates
- **Delete files** with cascade cleanup
- **Upload files** from user's computer
- **File path validation** to prevent duplicates within repos

### 👥 User Features
- **User profiles** with registration and management
- **Dashboard** showing owned and public repositories
- **Password reset flow** with multi-step OTP verification
- **Session-based authentication** for persistent login

---

## Tech Stack

### Backend
| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Django | 5.2 |
| Authentication | Firebase Admin SDK | Latest |
| Database | SQLite3 (Dev) / PostgreSQL (Prod) | - |
| ORM | Django ORM | Built-in |
| Email Backend | SMTP (Gmail) | - |
| Session Engine | Signed Cookies | Built-in |

### Frontend
| Component | Technology | Details |
|-----------|-----------|---------|
| Templating | Django Templates | Jinja2 syntax |
| Styling | CSS3 | Vanilla CSS |
| Interactivity | Vanilla JavaScript | ES6+ |
| HTTP Requests | Fetch API | AJAX requests |
| Code Editor | Textarea elements | Plain text editor |

### External Services
- **Firebase Authentication** - User management & authentication
- **Gmail SMTP** - Email delivery for OTP codes
- **Matplotlib** - Graph and plot generation

---

## Project Structure

```
Codehub/                              # Repository root
│
├─ codehub/                           # Django project directory
│  ├─ manage.py                       # Django management script
│  │
│  ├─ codehub/                        # Project configuration (previously codehubdebug)
│  │  ├─ __init__.py                  # Package initialization
│  │  ├─ settings.py                  # Django settings & configuration
│  │  ├─ urls.py                      # Main URL router
│  │  ├─ asgi.py                      # ASGI application (async)
│  │  └─ wsgi.py                      # WSGI application (production)
│  │
│  ├─ accounts/                       # User authentication app
│  │  ├─ admin.py                     # Django admin configuration
│  │  ├─ apps.py                      # App configuration
│  │  ├─ models.py                    # Data models (empty - uses Firebase)
│  │  ├─ urls.py                      # Authentication routes
│  │  ├─ views.py                     # Auth views (register, login, password reset)
│  │  ├─ tests.py                     # Unit tests
│  │  └─ migrations/                  # Database migration files
│  │
│  ├─ core/                           # Repository & code execution app
│  │  ├─ admin.py                     # Admin interface
│  │  ├─ apps.py                      # App configuration
│  │  ├─ models.py                    # Repository & RepoFile models
│  │  ├─ urls.py                      # Core routes
│  │  ├─ views.py                     # Core views (dashboard, repos, code execution)
│  │  ├─ tests.py                     # Unit tests
│  │  └─ migrations/                  # Migration files
│  │
│  ├─ shared/                         # Cross-app utilities & shared views
│  │  ├─ admin.py                     # Shared admin
│  │  ├─ apps.py                      # App configuration
│  │  ├─ models.py                    # Shared models (if any)
│  │  ├─ urls.py                      # Shared routes
│  │  ├─ views.py                     # Shared views
│  │  ├─ tests.py                     # Tests
│  │  └─ migrations/                  # Migrations
│  │
│  ├─ templates/                      # HTML templates
│  │  ├─ base.html                    # Base template with navbar/footer
│  │  ├─ index.html                   # Homepage
│  │  │
│  │  ├─ login.html                   # Login form
│  │  ├─ registration.html            # User registration form
│  │  ├─ forgotpassword.html          # Forgot password request
│  │  ├─ verify_otp.html              # OTP verification page
│  │  ├─ reset_password.html          # New password entry
│  │  ├─ profile.html                 # User profile page
│  │  │
│  │  ├─ dashboard.html               # User's repository dashboard
│  │  ├─ createrepo.html              # Create new repository form
│  │  ├─ repository_detail.html       # View repository files
│  │  ├─ repository_settings.html     # Repository settings/management
│  │  ├─ edit_repository.html         # Edit repo details
│  │  │
│  │  ├─ create_file.html             # Create new file in repo
│  │  ├─ edit_file.html               # Edit file content
│  │  ├─ upload_file.html             # Upload file form
│  │  │
│  │  └─ python_environment.html      # Python code execution interface
│  │
│  ├─ static/                         # Static assets
│  │  ├─ global.css                   # Global styles & resets
│  │  ├─ navbar.css                   # Navigation bar styling
│  │  ├─ index.css                    # Homepage styles
│  │  ├─ auth.css                     # Authentication page styles
│  │  ├─ dashboard.css                # Dashboard & repo styles
│  │  ├─ createrepo.css               # Create/edit repo styles
│  │  └─ scripts.js                   # Client-side JavaScript
│  │
│  ├─ db.sqlite3                      # Development database (local only)
│  ├─ .env                            # Environment variables (NOT in Git)
│  ├─ .env.example                    # Example .env template (in Git)
│  ├─ firebase_credentials.json       # Firebase admin credentials (NOT in Git)
│  ├─ firebase_credentials.example.json # Example credentials template (in Git)
│  ├─ requirements.txt                # Python dependencies
│  └─ manage.py                       # Django CLI
│
└─ venv/                              # Python virtual environment (NOT in Git)
```

### Key Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `accounts/` | Handles user authentication, registration, login, password reset |
| `core/` | Repository management, file operations, Python code execution |
| `shared/` | Utilities and views shared across multiple apps |
| `templates/` | HTML files rendered by Django views |
| `static/` | CSS, JavaScript, images served to the browser |

---

## Prerequisites

### System Requirements
- **Python 3.9+** (tested with Python 3.10+)
- **pip** (Python package manager)
- **Git** (for version control)
- **Firebase Project** (with authentication enabled)
- **Gmail Account** (for SMTP email functionality)

### Required Accounts
1. **Firebase Console** - Create a new project at [Firebase Console](https://console.firebase.google.com)
2. **Gmail Account** - With "App Passwords" enabled for SMTP access
3. **GitHub Account** (optional) - For source code version control

### Browser Compatibility
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

---

## Installation & Setup

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/ronakshah20/Codehub.git
cd Codehub/codehub
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Ensure pip is updated
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt

# Expected packages (approx):
# - Django==5.2
# - firebase-admin==latest
# - requests==latest
# - python-dotenv==latest
# - matplotlib==latest
# - (and other dependencies)
```

### 4. Environment Configuration

#### Create `.env` file

Copy the template and add your actual credentials:

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

#### `.env` Contents

```env
# Firebase Configuration
FIREBASE_WEB_API_KEY="YOUR_WEB_API_KEY"
FIREBASE_AUTH_DOMAIN="your-project.firebaseapp.com"
FIREBASE_PROJECT_ID="your-project-id"
FIREBASE_STORAGE_BUCKET="your-project.firebasestorage.app"
FIREBASE_MESSAGING_SENDER_ID="your-sender-id"
FIREBASE_APP_ID="your-app-id"

# Email Configuration (Gmail)
EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-app-password"  # NOT your Gmail password!
```

### 5. Firebase Setup

#### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click **"Add Project"** and enter "codehub"
3. Enable **Google Analytics** (optional)
4. Wait for project creation

#### Step 2: Enable Firebase Authentication
1. Go to **Authentication** → **Sign-in method**
2. Enable **Email/Password** provider
3. Click **Save**

#### Step 3: Get Web API Key
1. Go to **Project Settings** → **General**
2. Copy the Web API Key (in the "firebaseConfig" section)
3. Paste it in `.env` as `FIREBASE_WEB_API_KEY`

#### Step 4: Download Service Account Key (for Admin SDK)
1. Go to **Project Settings** → **Service Accounts**
2. Click **"Generate New Private Key"**
3. Save the downloaded JSON as `firebase_credentials.json` in the project root

#### Step 5: Initialize Firebase Admin SDK
```bash
# This happens automatically when Django loads
# The settings.py file initializes Firebase Admin SDK with the service account key
```

### 6. Email Configuration

#### Get Gmail App Password

Firebase uses SMTP to send OTP emails. You need a Gmail **App Password** (not your regular password):

1. Enable **2-Factor Authentication** on your Google account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Find **"App passwords"** section
4. Select **"Mail"** and **"Windows Computer"** (or your device)
5. Google will generate a 16-character password
6. Copy this password to `.env` as `EMAIL_HOST_PASSWORD`

**Example**: `EMAIL_HOST_PASSWORD="dpiy rkne mxos ikhj"`

#### Test Email Configuration
```bash
# Run Django shell
python manage.py shell

# Send test email
from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test message',
    'your-email@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
```

### 7. Database Migrations

```bash
# Create database tables
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Verify tables were created
python manage.py dbshell
# Then type: .tables
```

### 8. Run the Development Server

```bash
# Start Django development server
python manage.py runserver

# Server will be running at: http://127.0.0.1:8000/

# Access the application
# Home: http://localhost:8000/
# Dashboard: http://localhost:8000/dashboard/
# Admin Panel: http://localhost:8000/admin/
```

---

## Usage Guide

### Authentication Workflow

#### User Registration
1. Navigate to `/accounts/register/`
2. Enter username, email, password
3. Click "Register"
4. User is created in Firebase and Django database
5. Redirected to login page

#### User Login
1. Go to `/accounts/login/`
2. Enter email and password
3. Firebase verifies credentials via REST API
4. Django creates a session for the user
5. Redirected to dashboard

#### Password Reset (OTP Flow)
1. **Step 1**: User clicks "Forgot Password?" on login page
2. **Step 2**: Enters email address
3. **Step 3**: OTP (6-digit code) is emailed to user
4. **Step 4**: User enters OTP (valid for 5 minutes)
5. **Step 5**: User sets new password
6. **Step 6**: Password updated in Firebase
7. **Step 7**: User redirected to login with new password

**Key Security Features**:
- OTP expires after 5 minutes
- OTP stored in session (server-side)
- Password updated in Firebase (not bypassed)
- All steps require valid previous step

### Repository Management

#### Create Repository
1. Go to Dashboard (`/dashboard/`)
2. Click **"Create Repository"**
3. Fill in:
   - **Repository Name**: Unique within your account
   - **Description**: Optional project description
   - **Visibility**: Public (anyone can view) or Private (only you)
4. Click **"Create"**
5. Redirected to repository detail page

#### View Repository
1. Click on any repository from dashboard
2. See file listing in repository
3. Create, edit, upload, or delete files

#### Edit Repository
1. Open repository
2. Go to **"Settings"** tab
3. Update name, description, or visibility
4. Save changes

#### Delete Repository
1. Go to **"Settings"** tab
2. Click **"Delete Repository"**
3. Confirm deletion (irreversible)

### File Operations

#### Create File
1. Open repository
2. Click **"New File"**
3. Enter file path (e.g., `main.py`, `utils/helpers.py`)
4. Add file content in editor
5. Click **"Save"**

#### Edit File
1. Click on file in repository
2. Modify content in editor
3. Click **"Update"**
4. File timestamp updates automatically

#### Upload File
1. Click **"Upload File"** in repository
2. Select file from computer
3. Confirm upload
4. File stored in repository with original name

#### Delete File
1. Open file
2. Click **"Delete"**
3. File removed from repository

### Python Code Execution

#### Access Python Environment
1. Click **"Python Environment"** in navigation
2. Or go to `/core/python-environment/`

#### Write and Execute Code
1. Type Python code in the editor
2. Click **"Run Code"** button
3. Code executes on server in isolated context
4. Output displays in real-time

#### Features

**Standard Output**:
```python
# Print statements appear in output
print("Hello, World!")
print("Result:", 2 + 2)
# Output: Hello, World!
#         Result: 4
```

**Matplotlib Plots**:
```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [1, 4, 9, 16]
plt.plot(x, y)
plt.show()
# Plot displays as PNG image in output
```

**User Input**:
```python
# input() pauses execution and asks for user input
name = input("Enter your name: ")
print(f"Hello, {name}!")
# Server prompts for input, returns from UI
```

**Error Handling**:
```python
# Syntax errors and runtime errors are caught
# Error message displayed with traceback
result = 1 / 0  # ZeroDivisionError
# Output: --- EXECUTION ERROR ---
#         ZeroDivisionError: division by zero
```

---

## Contributing

### How to Contribute

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**: `git commit -m "Add feature: description"`
5. **Push to your fork**: `git push origin feature/your-feature`
6. **Create Pull Request** with detailed description

### Reporting Issues

Use GitHub Issues to report bugs:
1. Clear, descriptive title
2. Steps to reproduce
3. Expected vs actual behavior
4. Screenshots if applicable
5. Python/Django versions

### Feature Requests

Propose new features via Issues with:
- Use case description
- Proposed solution
- Alternative approaches considered

---

## License

This project is licensed under the [**MIT License**](./LICENSE) - see LICENSE file for details.

---

## Acknowledgments

- Django Framework and community
- Firebase by Google
- Matplotlib for visualization
- Open source contributors

---

## Final Notes

- **Keep `.env` and `firebase_credentials.json` secure** - never commit them!
- **Test thoroughly before deployment** - especially authentication flows
- **Monitor logs** for errors and security issues
- **Keep dependencies updated** - `pip list --outdated`
- **Enable HTTPS** for production - use Let's Encrypt (free SSL)
- **Regular backups** - set up automated database backups

---

**Last Updated**: December 19, 2025
**Status**: Production Ready
