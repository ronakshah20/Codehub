# CodeHub

CodeHub is a Django-based web application that provides GitHub-like repository management with an integrated Python execution environment and Firebase-backed authentication.

## Features

### Authentication & Accounts

- User registration with Firebase Authentication and mirrored Django `User` for session handling.
- Email/password login via Firebase REST API (`signInWithPassword`).
- Django session login using the Firebase `localId` as the Django username.
- Profile page for logged-in users.
- Logout that clears the Django session.
- Full 3-step password reset flow:
  1. **Forgot Password** – user enters email.
  2. **OTP Verification** – OTP is emailed and validated with session-based expiry.
  3. **Password Reset** – password updated in Firebase Auth via Admin SDK.

### Repository Management

- Create repositories with:
  - Name
  - Description
  - Visibility (`public` / `private`)
- Dashboard:
  - Lists repositories owned by the user (any visibility).
  - Shows public repositories owned by other users.
- Repository detail view:
  - Browse repository files.
  - Download repository as ZIP.
- Repository settings:
  - Edit repository details.
  - Delete repository.

### File Management within Repositories

- Create new files in a repository.
- Edit existing files (by `file_id`).
- Delete files.
- Upload files into a repository.
- Dedicated templates for:
  - `create_file.html`
  - `edit_file.html`
  - `upload_file.html`

### Integrated Python Environment

- Dedicated **Python Environment** page:
  - Write and run arbitrary Python code in the browser.
  - Support for:
    - Capturing `stdout`.
    - Handling `input()` via a custom input-capturing context manager.
    - Generating Matplotlib plots and returning them as base64-encoded images.
- Backend API endpoint:
  - `POST /api/run-code/` accepts:
    - `code`: Python source.
    - `inputs`: list of simulated `input()` values.
    - `input_index`: current index into inputs list.
  - Returns JSON with:
    - Execution status.
    - Output text.
    - Plot image (base64) if generated.
    - Information when more `input()` is required.

### UI & Frontend

- Base template with shared navbar, branding, and auth-aware navigation.
- Separate templates for:
  - Landing page (`index.html`).
  - Dashboard.
  - Auth pages (login, registration, forgot password, OTP verify, reset password).
  - Repository and file operations.
- Static assets:
  - Multiple CSS files (`global.css`, `navbar.css`, `index.css`, `dashboard.css`, `auth.css`, `createrepo.css`, etc.).
  - `scripts.js` for UI enhancements (e.g., button ripple effects, navbar scroll behavior).

---

## Project Structure

The recommended structure (matching your current layout and GitHub expectations) is:
Codehub/ # Repo root (downloaded folder)
│
├─ codehub/ # Django project directory
│ ├─ manage.py
│ │
│ ├─ codehubdebug/ # Project config package
│ │ ├─ init.py
│ │ ├─ settings.py
│ │ ├─ urls.py
│ │ ├─ asgi.py
│ │ └─ wsgi.py
│ │
│ ├─ accounts/ # Accounts app
│ │ ├─ admin.py
│ │ ├─ apps.py
│ │ ├─ models.py
│ │ ├─ urls.py
│ │ ├─ views.py
│ │ └─ migrations/
│ │
│ ├─ core/ # Core app (repos, files, python env)
│ │ ├─ admin.py
│ │ ├─ apps.py
│ │ ├─ models.py
│ │ ├─ urls.py
│ │ ├─ views.py
│ │ └─ migrations/
│ │
│ ├─ shared/ # Shared utilities / cross‑app views
│ │ ├─ views.py
│ │ ├─ urls.py
│ │ ├─ models.py
│ │ ├─ admin.py
│ │ ├─ apps.py
│ │ ├─ tests.py
│ │ └─ migrations/
│ │
│ ├─ templates/ # HTML templates
│ │ ├─ base.html
│ │ ├─ index.html
│ │ ├─ login.html
│ │ ├─ registration.html
│ │ ├─ forgotpassword.html
│ │ ├─ verify_otp.html
│ │ ├─ reset_password.html
│ │ ├─ dashboard.html
│ │ ├─ createrepo.html
│ │ ├─ repository_detail.html
│ │ ├─ repository_settings.html
│ │ ├─ edit_repository.html
│ │ ├─ create_file.html
│ │ ├─ edit_file.html
│ │ ├─ upload_file.html
│ │ ├─ python_environment.html
│ │ └─ profile.html
│ │
│ ├─ static/ # Static assets
│ │ ├─ global.css
│ │ ├─ navbar.css
│ │ ├─ index.css
│ │ ├─ dashboard.css
│ │ ├─ auth.css
│ │ ├─ createrepo.css
│ │ └─ scripts.js
│ │
│ ├─ db.sqlite3 # Local DB (optional in Git)
│ ├─ .env # REAL env file (ignored in Git)
│ ├─ firebase_credentials.json # REAL Firebase creds (ignored)
│ ├─ .env.example # Template (committed)
│ ├─ firebase_credentials.example.json # Template (committed)
│ └─ requirements.txt
│
└─ venv/ # Local virtualenv (not committed)

---

## Technology stack

- **Backend:** Django 5.x, Python 3.11+ [file:52]  
- **Auth:** Firebase Authentication (REST + Admin SDK) [file:54]  
- **Database (dev):** SQLite (Django default), file `db.sqlite3` [file:52]  
- **Frontend:** HTML templates + CSS/JS static assets  
- **Email:** SMTP (Gmail) for password reset emails [file:52]

---

## Installation

### 1. Clone the repository
- These steps are for someone who wants to run their **own local copy**. End‑users only need the deployed URL.
    ```bash
    git clone https://github.com/ronakshah22-lab/Codehub.git
    cd Codehub/codehub

### 2. Create and activate a virtual environment
    ```bash
    python -m venv venv

- Windows:
    ```bash
    venv/Scripts/activate

- Linux/macOS:
    ```bash
    source venv/bin/activate

### 3. Install dependencies
    ```bash
    pip install -r requirements.txt

---

## Configuration

### Environment Variables (`.env`)

- Create `.env` in `codehub/` (same folder as `manage.py`) using `.env.example` as a template:
    ```bash
    cp .env.example .env

- Edit `.env` with your real values:

FIREBASE_WEB_API_KEY="your-web-api-key"
FIREBASE_AUTH_DOMAIN="your-project-id.firebaseapp.com"
FIREBASE_PROJECT_ID="your-project-id"
FIREBASE_STORAGE_BUCKET="your-project-id.firebasestorage.app"
FIREBASE_MESSAGING_SENDER_ID="..."
FIREBASE_APP_ID="1:...:web:..."

EMAIL_HOST_USER="your-email@gmail.com"
EMAIL_HOST_PASSWORD="your-gmail-app-password"

- `settings.py` already loads `.env` using `python-dotenv` (`dotenv.load_dotenv`), and uses these values for Firebase REST authentication and Django email backend.

### Firebase Admin Credentials

1. In the Firebase console, create a **service account** key for Admin SDK.
2. Download the JSON file and save it in:
**Codehub/codehub/firebase_credentials.json**
3. Ensure this file is **ignored** by Git (listed in `.gitignore`).
4. Initialize Firebase Admin in your code (already present in your project via `firebase_admin.auth` usage) by pointing to this file path or environment variable.

---

## Database Setup

- Run migrations:
   ```bash
   python manage.py migrate

- You can create a superuser if needed:
   ```bash
   python manage.py createsuperuser

---

## Running the Development Server

- From `codehub/` (folder containing `manage.py`):
   ```bash
   python manage.py runserver


The app will be available at:

- `http://127.0.0.1:8000/` – Landing page
- `http://127.0.0.1:8000/accounts/register/` – Registration
- `http://127.0.0.1:8000/accounts/login/` – Login
- `http://127.0.0.1:8000/dashboard/` – Dashboard (after login)
- `http://127.0.0.1:8000/python-env/` – Python environment

---

## Usage Overview

### Authentication Flow

1. **Register** at `/accounts/register/`:
   - Creates user in Firebase Auth.
   - Creates mirrored Django `User` (with `uid` as username) for session-based auth.

2. **Login** at `/accounts/login/`:
   - Uses Firebase REST API with `FIREBASE_WEB_API_KEY` to validate credentials.
   - On success, retrieves `localId`, looks up Django `User`, and calls `login(request, user)`.

3. **Forgot Password**:
   - `/accounts/forgot-password/` – enter email.
   - Backend:
     - Looks up Firebase user by email.
     - Generates OTP.
     - Stores OTP and timestamp in session.
     - Sends email using Django email backend.
   - `/accounts/verify-otp/` – user enters OTP.
   - `/accounts/reset-password/` – user sets new password.
   - Final step calls `firebase_admin.auth.update_user` to update password in Firebase Auth.[web:24]

### Repositories & Files

- **Create repository** at `/create/`.
- **View dashboard** at `/dashboard/`.
- **View repository** at:
  - `/<username>/<repo_name>/`
- **Repository settings**:
  - `/<username>/<repo_name>/settings/`
- **Edit repository**:
  - `/<username>/<repo_name>/edit-repo/`
- **Delete repository**:
  - `/<username>/<repo_name>/delete-repo/`
- **Download repository**:
  - `/<username>/<repo_name>/download/`
- **File operations**:
  - Create: `/<username>/<repo_name>/create/`
  - Edit: `/<username>/<repo_name>/edit/<file_id>/`
  - Delete: `/<username>/<repo_name>/delete/<file_id>/`
  - Upload: `/<username>/<repo_name>/upload/`

All repository and file routes are protected with `@login_required(login_url='/accounts/login/')` to ensure only authenticated users access them.

### Python Environment

- Navigate to `/python-env/` (requires login).
- Use the frontend editor to send code to `POST /api/run-code/`.
- The backend:
  - Captures output via `contextlib.redirect_stdout`.
  - Intercepts `input()` calls via a custom `CapturingInput` context manager.
  - Renders Matplotlib plots into an in-memory buffer and returns them as base64 PNG.

---

## Static Files

- Development:
  - Served from `STATICFILES_DIRS = [BASE_DIR / 'static']`.
- Production:
  - Run:

    ```bash
       python manage.py collectstatic

  - This collects all static files into `STATIC_ROOT = BASE_DIR / 'staticfiles'` for serving by a real web server.[web:35][web:36][web:40]

---

## Environment & Secrets

**Do not commit:**

- `.env`
- `firebase_credentials.json`
- `db.sqlite3` (optional)
- `venv/`
- `staticfiles/` (collectstatic output)

Use `.env.example` and `firebase_credentials.example.json` as templates to show users what they must provide.

---

## Testing

You currently have basic `tests.py` stubs in both `accounts` and `core`. To run tests:
```bash
   python manage.py test


You can gradually add unit tests for views (e.g., auth flow, repository CRUD, Python environment API).

---

## Deployment Notes (High-Level)

- Use a production WSGI/ASGI server (Gunicorn/Uvicorn) behind Nginx/Apache.[web:35][web:40]
- Configure:
  - `DEBUG = False`
  - Proper `ALLOWED_HOSTS`
  - Separate production `.env` with secure values.
- Use a persistent database (PostgreSQL/MySQL) in production.
- Set up static and media files serving according to your hosting provider’s guide.

---

## License

Add your preferred license here (e.g., MIT, Apache 2.0).