from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pymysql
import pymysql.cursors
from functools import wraps
import hashlib
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'gwpc_secret_key_2024'

# MySQL Configuration - Update these with your credentials
aDB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'college_mgmt',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db():
    """Get database connection"""
    return pymysql.connect(**DB_CONFIG)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ─── AUTH ────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = hash_password(data.get('password'))
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            return jsonify({'success': True, 'role': user['role']})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# ─── DASHBOARD STATS ─────────────────────────────────────
@app.route('/api/stats')
@login_required
def get_stats():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM students WHERE status='active'")
    students = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM faculty WHERE status='active'")
    faculty = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM courses")
    courses = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM departments")
    departments = cur.fetchone()['count']
    cur.close()
    conn.close()
    return jsonify({'students': students, 'faculty': faculty, 'courses': courses, 'departments': departments})

# ─── STUDENTS ────────────────────────────────────────────
@app.route('/students')
@login_required
def students():
    return render_template('students.html')

@app.route('/api/students', methods=['GET'])
@login_required
def get_students():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.*, d.name as department_name 
        FROM students s 
        LEFT JOIN departments d ON s.department_id = d.id
        ORDER BY s.created_at DESC
    """)
    students = cur.fetchall()
    cur.close()
    conn.close()
    for s in students:
        if s.get('dob'):
            s['dob'] = s['dob'].strftime('%Y-%m-%d')
        if s.get('created_at'):
            s['created_at'] = s['created_at'].strftime('%Y-%m-%d')
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
@login_required
def add_student():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (enrollment_no, full_name, email, phone, dob, address, department_id, semester, year_of_admission, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'active')
    """, (d['enrollment_no'], d['full_name'], d['email'], d['phone'], d['dob'], d['address'], d['department_id'], d['semester'], d['year_of_admission']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Student added successfully'})

@app.route('/api/students/<int:id>', methods=['PUT'])
@login_required
def update_student(id):
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE students SET full_name=%s, email=%s, phone=%s, dob=%s, address=%s,
        department_id=%s, semester=%s, status=%s WHERE id=%s
    """, (d['full_name'], d['email'], d['phone'], d['dob'], d['address'], d['department_id'], d['semester'], d['status'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Student updated'})

@app.route('/api/students/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE students SET status='inactive' WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Student removed'})

# ─── FACULTY ─────────────────────────────────────────────
@app.route('/faculty')
@login_required
def faculty():
    return render_template('faculty.html')

@app.route('/api/faculty', methods=['GET'])
@login_required
def get_faculty():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.*, d.name as department_name 
        FROM faculty f 
        LEFT JOIN departments d ON f.department_id = d.id
        ORDER BY f.created_at DESC
    """)
    faculty = cur.fetchall()
    cur.close()
    conn.close()
    for f in faculty:
        if f.get('joining_date'):
            f['joining_date'] = f['joining_date'].strftime('%Y-%m-%d')
        if f.get('created_at'):
            f['created_at'] = f['created_at'].strftime('%Y-%m-%d')
    return jsonify(faculty)

@app.route('/api/faculty', methods=['POST'])
@login_required
def add_faculty():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO faculty (employee_id, full_name, email, phone, designation, department_id, qualification, joining_date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'active')
    """, (d['employee_id'], d['full_name'], d['email'], d['phone'], d['designation'], d['department_id'], d['qualification'], d['joining_date']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Faculty added successfully'})

@app.route('/api/faculty/<int:id>', methods=['PUT'])
@login_required
def update_faculty(id):
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE faculty SET full_name=%s, email=%s, phone=%s, designation=%s,
        department_id=%s, qualification=%s, status=%s WHERE id=%s
    """, (d['full_name'], d['email'], d['phone'], d['designation'], d['department_id'], d['qualification'], d['status'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Faculty updated'})

@app.route('/api/faculty/<int:id>', methods=['DELETE'])
@login_required
def delete_faculty(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE faculty SET status='inactive' WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Faculty removed'})

# ─── DEPARTMENTS ─────────────────────────────────────────
@app.route('/departments')
@login_required
def departments():
    return render_template('departments.html')

@app.route('/api/departments', methods=['GET'])
@login_required
def get_departments():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.*, 
               (SELECT COUNT(*) FROM students s WHERE s.department_id=d.id AND s.status='active') as student_count,
               (SELECT COUNT(*) FROM faculty f WHERE f.department_id=d.id AND f.status='active') as faculty_count
        FROM departments d ORDER BY d.name
    """)
    depts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(depts)

@app.route('/api/departments', methods=['POST'])
@login_required
def add_department():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO departments (name, code, description, hod) VALUES (%s, %s, %s, %s)",
                (d['name'], d['code'], d['description'], d['hod']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Department added'})

@app.route('/api/departments/<int:id>', methods=['PUT'])
@login_required
def update_department(id):
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE departments SET name=%s, code=%s, description=%s, hod=%s WHERE id=%s",
                (d['name'], d['code'], d['description'], d['hod'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Department updated'})

@app.route('/api/departments/<int:id>', methods=['DELETE'])
@login_required
def delete_department(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM departments WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Department deleted'})

# ─── COURSES ─────────────────────────────────────────────
@app.route('/courses')
@login_required
def courses():
    return render_template('courses.html')

@app.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.*, d.name as department_name, f.full_name as faculty_name
        FROM courses c
        LEFT JOIN departments d ON c.department_id = d.id
        LEFT JOIN faculty f ON c.faculty_id = f.id
        ORDER BY c.name
    """)
    courses = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(courses)

@app.route('/api/courses', methods=['POST'])
@login_required
def add_course():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO courses (name, code, department_id, faculty_id, semester, credits, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (d['name'], d['code'], d['department_id'], d.get('faculty_id'), d['semester'], d['credits'], d['description']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Course added'})

@app.route('/api/courses/<int:id>', methods=['PUT'])
@login_required
def update_course(id):
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE courses SET name=%s, code=%s, department_id=%s, faculty_id=%s,
        semester=%s, credits=%s, description=%s WHERE id=%s
    """, (d['name'], d['code'], d['department_id'], d.get('faculty_id'), d['semester'], d['credits'], d['description'], id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Course updated'})

@app.route('/api/courses/<int:id>', methods=['DELETE'])
@login_required
def delete_course(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM courses WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Course deleted'})

# ─── ATTENDANCE ───────────────────────────────────────────
@app.route('/attendance')
@login_required
def attendance():
    return render_template('attendance.html')

@app.route('/api/attendance', methods=['GET'])
@login_required
def get_attendance():
    department_id = request.args.get('department_id')
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    conn = get_db()
    cur = conn.cursor()
    query = """
        SELECT a.*, s.full_name, s.enrollment_no, c.name as course_name
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        JOIN courses c ON a.course_id = c.id
        WHERE a.date = %s
    """
    params = [date]
    if department_id:
        query += " AND s.department_id = %s"
        params.append(department_id)
    cur.execute(query, params)
    records = cur.fetchall()
    cur.close()
    conn.close()
    for r in records:
        if r.get('date'):
            r['date'] = r['date'].strftime('%Y-%m-%d')
    return jsonify(records)

@app.route('/api/attendance', methods=['POST'])
@login_required
def mark_attendance():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    for record in d['records']:
        cur.execute("""
            INSERT INTO attendance (student_id, course_id, date, status)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE status=%s
        """, (record['student_id'], d['course_id'], d['date'], record['status'], record['status']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Attendance marked'})

@app.route('/api/attendance/summary')
@login_required
def attendance_summary():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.full_name, s.enrollment_no, d.name as department,
               COUNT(CASE WHEN a.status='present' THEN 1 END) as present,
               COUNT(a.id) as total,
               ROUND(COUNT(CASE WHEN a.status='present' THEN 1 END)*100.0/NULLIF(COUNT(a.id),0),1) as percentage
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        LEFT JOIN departments d ON s.department_id = d.id
        WHERE s.status='active'
        GROUP BY s.id ORDER BY s.full_name
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

# ─── MARKS / RESULTS ──────────────────────────────────────
@app.route('/marks')
@login_required
def marks():
    return render_template('marks.html')

@app.route('/api/marks', methods=['GET'])
@login_required
def get_marks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.*, s.full_name, s.enrollment_no, c.name as course_name, d.name as dept_name
        FROM marks m
        JOIN students s ON m.student_id = s.id
        JOIN courses c ON m.course_id = c.id
        LEFT JOIN departments d ON s.department_id = d.id
        ORDER BY s.full_name
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/marks', methods=['POST'])
@login_required
def add_marks():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO marks (student_id, course_id, exam_type, marks_obtained, max_marks, semester)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE marks_obtained=%s
    """, (d['student_id'], d['course_id'], d['exam_type'], d['marks_obtained'], d['max_marks'], d['semester'], d['marks_obtained']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Marks saved'})

# ─── NOTICES ─────────────────────────────────────────────
@app.route('/notices')
@login_required
def notices():
    return render_template('notices.html')

@app.route('/api/notices', methods=['GET'])
@login_required
def get_notices():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT n.*, u.full_name as posted_by_name
        FROM notices n JOIN users u ON n.posted_by = u.id
        ORDER BY n.created_at DESC
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    for n in data:
        if n.get('created_at'):
            n['created_at'] = n['created_at'].strftime('%Y-%m-%d %H:%M')
        if n.get('expiry_date'):
            n['expiry_date'] = n['expiry_date'].strftime('%Y-%m-%d')
    return jsonify(data)

@app.route('/api/notices', methods=['POST'])
@login_required
def add_notice():
    d = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notices (title, content, category, posted_by, expiry_date)
        VALUES (%s, %s, %s, %s, %s)
    """, (d['title'], d['content'], d['category'], session['user_id'], d.get('expiry_date')))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Notice posted'})

@app.route('/api/notices/<int:id>', methods=['DELETE'])
@login_required
def delete_notice(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM notices WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Notice deleted'})

# ─── HELPER APIs ─────────────────────────────────────────
@app.route('/api/departments/list')
@login_required
def dept_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, code FROM departments ORDER BY name")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/faculty/list')
@login_required
def faculty_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, designation FROM faculty WHERE status='active' ORDER BY full_name")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/students/list')
@login_required
def students_list():
    dept = request.args.get('department_id')
    conn = get_db()
    cur = conn.cursor()
    if dept:
        cur.execute("SELECT id, full_name, enrollment_no FROM students WHERE status='active' AND department_id=%s ORDER BY full_name", (dept,))
    else:
        cur.execute("SELECT id, full_name, enrollment_no FROM students WHERE status='active' ORDER BY full_name")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/courses/list')
@login_required
def courses_list():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, name, code FROM courses ORDER BY name")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/session')
def get_session():
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'role': session['role'], 'full_name': session['full_name'], 'username': session['username']})
    return jsonify({'logged_in': False})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
