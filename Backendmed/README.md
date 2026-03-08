# MedMeet - Medical Appointment & Pharmacy Management System

A Django-based full-stack application for managing hospitals, doctors, appointments, and pharmacy services.

> Run all Django commands from the `Backendmed/` directory (the folder containing `manage.py`).

## Quick Start

### Prerequisites
- Python 3.11+ installed
- pip package manager

### One-Command Setup & Run

**On Windows:**
```powershell
py -3 -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; python manage.py migrate; python manage.py runserver
```

**On macOS/Linux:**
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```

The app will be available at: http://127.0.0.1:8000/

---

## Manual Setup (Step-by-Step)

### 1. Create Virtual Environment
```bash
# Windows
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
When prompted, enter:
- **Username**: `admin`
- **Email**: `admin@medmeet.com`
- **Password**: `admin123` (or your preferred password)

### 5. Start Development Server
```bash
python manage.py runserver
```

---

## Access Points

### Admin Panel
- URL: `http://127.0.0.1:8000/admin/`
- Login with superuser credentials (created above)

### Frontend (Patient Portal)
- URL: `http://127.0.0.1:8000/frontendmed/Med_Meet/`
- Features: Browse hospitals, doctors, book appointments, view pharmacy

### Backend (Admin Dashboard)
- URL: `http://127.0.0.1:8000/Backendmed/back_main/`
- Features: Manage doctors, hospitals, departments, appointments, blogs, pharmacy

---

## Project Structure

```
Backendmed/
├── Backendmed/              # Project configuration
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py
├── medapp/                  # Backend/Admin app
│   ├── models.py            # Database models
│   ├── views.py             # Admin views
│   ├── urls.py              # Backend routes
│   └── templates/           # Admin templates
├── MedMeet/                 # Frontend app
│   ├── models.py            # User/signup models
│   ├── views.py             # Frontend views
│   ├── urls.py              # Frontend routes
│   └── templates/           # Public templates
├── media/                   # Uploaded files (images)
├── db.sqlite3               # Database
├── manage.py                # Django CLI
└── requirements.txt         # Dependencies
```

---

## Key Features

### Admin Dashboard
- **Doctors**: Add, edit, delete doctor profiles
- **Hospitals**: Manage hospitals and departments
- **Departments**: Configure medical departments
- **Appointments**: View and manage patient appointments
- **Pharmacy**: Manage medicines and inventory
- **Countries**: Manage service locations
- **Blogs**: Write and manage blog posts

### Patient Portal
- **Browse**: View available hospitals and doctors
- **Services**: Explore pharmacy store
- **Appointments**: Book appointments online
- **Accounts**: Sign up, login, manage profile

---

## Available Routes

### Admin Routes (Backend)
- `/Backendmed/back_main/` - Dashboard
- `/Backendmed/add_doctor/` - Add doctor
- `/Backendmed/display_doctor/` - View all doctors
- `/Backendmed/add_hosp/` - Add hospital
- `/Backendmed/display_hospital/` - View hospitals
- `/Backendmed/add_appointment/` - Create appointment
- `/Backendmed/display_appointment/` - View appointments
- `/Backendmed/add_pharmacy/`- Add pharmacy/medicine
- `/Backendmed/display_medicine/` - View pharmacy
- `/Backendmed/add_blog/` - Add blog
- `/Backendmed/display_blog/` - View blogs

### Patient Routes (Frontend)
- `/frontendmed/Med_Meet/` - Home
- `/frontendmed/About_med/` - About us
- `/frontendmed/Hospital_med/` - Browse hospitals
- `/frontendmed/Blog_med/` - Read blogs
- `/frontendmed/Pharmacy_med/` - Shop pharmacy
- `/frontendmed/Login_customer/` - Patient login/signup
- `/frontendmed/Contacts_med/` - Contact us

---

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8080
# Access at http://127.0.0.1:8080/
```

### Database Errors
```bash
# Reset database (clears all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Template Not Found Error
Ensure all templates are in the correct `templates/` directories within each app.

---

## Default Test Data

After setup, log in to the admin panel to:
1. Add countries first
2. Add departments
3. Add hospitals with departments
4. Add doctors linked to hospitals
5. Add medicines to pharmacy

---

## Technologies Used

- **Python 3.11+**
- **Django 5.1+**
- **SQLite3** (database)
- **Pillow** (image handling)
- **HTML/CSS/JavaScript** (frontend)

---

## Notes

- Files are uploaded to `/media/` directory
- All images are automatically stored in categorized subdirectories
- Login credentials use hashed passwords
- Sessions are managed via Django session framework

---

## Support

For issues, check the Django logs in the console output when running `runserver`.

