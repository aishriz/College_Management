# Government Women Polytechnic College
# College Management System

A full-stack web application built with **Flask** (Python), **MySQL**, and **HTML/CSS/JS**.

---

## Features
- 🎓 **Student Management** – Add, edit, search, filter students
- 👩‍🏫 **Faculty Management** – Manage faculty records and assignments
- 🏛️ **Departments** – Department-wise view with stats
- 📚 **Courses** – Course catalog with faculty assignment
- ✅ **Attendance** – Mark & view attendance with percentage tracking
- 📊 **Marks & Results** – Enter marks, auto grade calculation
- 📢 **Notice Board** – Post and manage college notices
- 🔐 **Login System** – Session-based authentication

---

## Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

---

## Setup Instructions

### 1. Install Dependencies
```bash
cd college_mgmt
pip install -r requirements.txt
```

> On Linux, you may need: `sudo apt install libmysqlclient-dev`
> On macOS: `brew install mysql-client`

### 2. Create the Database
Open MySQL and run:
```bash
mysql -u root -p < schema.sql
```
This creates the database, all tables, and inserts sample data.

### 3. Configure Database Connection
Open `app.py` and update these lines:
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'  # ← Change this
app.config['MYSQL_DB'] = 'college_mgmt'
```

### 4. Run the Application
```bash
python app.py
```
Open your browser at: **http://localhost:5000**

---

## Default Login Credentials
| Username    | Password       | Role  |
|-------------|---------------|-------|
| admin       | admin123       | Admin |
| principal   | principal123   | Admin |

---

## Project Structure
```
college_mgmt/
├── app.py                  # Flask backend (all routes & API)
├── schema.sql              # MySQL database schema + seed data
├── requirements.txt        # Python dependencies
├── templates/
│   ├── base.html           # Shared layout with sidebar
│   ├── login.html          # Login page
│   ├── dashboard.html      # Dashboard with stats
│   ├── students.html       # Student management
│   ├── faculty.html        # Faculty management
│   ├── departments.html    # Department cards
│   ├── courses.html        # Course management
│   ├── attendance.html     # Attendance marking & summary
│   ├── marks.html          # Marks entry & results
│   └── notices.html        # Notice board
└── static/
    ├── css/main.css        # All styles (Navy & Gold theme)
    └── js/main.js          # Shared JS (modal, toast, sidebar)
```

---

## Tech Stack
- **Backend**: Python Flask, Flask-MySQLdb
- **Database**: MySQL 8
- **Frontend**: HTML5, CSS3 (custom design), Vanilla JavaScript
- **Icons**: Font Awesome 6
- **Fonts**: Playfair Display + DM Sans (Google Fonts)
