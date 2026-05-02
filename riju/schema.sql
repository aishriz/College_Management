-- ============================================================
--  GOVERNMENT WOMEN POLYTECHNIC COLLEGE
--  College Management System - Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS college_mgmt;
USE college_mgmt;

-- USERS
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'faculty', 'student') DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- DEPARTMENTS
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT,
    hod VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- STUDENTS
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollment_no VARCHAR(30) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    dob DATE,
    address TEXT,
    department_id INT,
    semester INT DEFAULT 1,
    year_of_admission YEAR,
    status ENUM('active', 'inactive', 'passed_out') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

-- FACULTY
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(30) UNIQUE NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    designation VARCHAR(100),
    department_id INT,
    qualification VARCHAR(200),
    joining_date DATE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL
);

-- COURSES
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    code VARCHAR(30) UNIQUE NOT NULL,
    department_id INT,
    faculty_id INT,
    semester INT,
    credits INT DEFAULT 3,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE SET NULL,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE SET NULL
);

-- ATTENDANCE
CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('present', 'absent', 'late') DEFAULT 'absent',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_attendance (student_id, course_id, date),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- MARKS
CREATE TABLE IF NOT EXISTS marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    exam_type ENUM('internal1', 'internal2', 'practical', 'final') NOT NULL,
    marks_obtained DECIMAL(5,2),
    max_marks DECIMAL(5,2) DEFAULT 100,
    semester INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_marks (student_id, course_id, exam_type),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- NOTICES
CREATE TABLE IF NOT EXISTS notices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    category ENUM('general', 'academic', 'exam', 'event', 'holiday') DEFAULT 'general',
    posted_by INT,
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (posted_by) REFERENCES users(id)
);

-- ============================================================
-- SEED DATA
-- ============================================================

-- Admin user (password: admin123)
INSERT INTO users (username, password, full_name, role) VALUES
('admin', SHA2('admin123', 256), 'Administrator', 'admin'),
('principal', SHA2('principal123', 256), 'Dr. Sunita Sharma', 'admin');

-- Departments (typical polytechnic departments)
INSERT INTO departments (name, code, description, hod) VALUES
('Computer Science & Engineering', 'CSE', 'Department of Computer Science and Engineering', 'Mrs. Priya Verma'),
('Electronics & Communication', 'ECE', 'Department of Electronics and Communication Engineering', 'Mrs. Rekha Singh'),
('Civil Engineering', 'CE', 'Department of Civil Engineering', 'Mrs. Anjali Mishra'),
('Mechanical Engineering', 'ME', 'Department of Mechanical Engineering', 'Mrs. Kavita Patel'),
('Electrical Engineering', 'EE', 'Department of Electrical Engineering', 'Mrs. Neeta Joshi');

-- Faculty
INSERT INTO faculty (employee_id, full_name, email, phone, designation, department_id, qualification, joining_date) VALUES
('FAC001', 'Mrs. Priya Verma', 'priya.verma@gwpc.edu.in', '9876543210', 'HOD & Lecturer', 1, 'M.Tech (CSE)', '2015-07-01'),
('FAC002', 'Mrs. Sunita Kumari', 'sunita.k@gwpc.edu.in', '9876543211', 'Lecturer', 1, 'B.Tech (CSE)', '2018-08-01'),
('FAC003', 'Mrs. Rekha Singh', 'rekha.singh@gwpc.edu.in', '9876543212', 'HOD & Lecturer', 2, 'M.Tech (ECE)', '2014-07-01'),
('FAC004', 'Mrs. Pooja Sharma', 'pooja.sharma@gwpc.edu.in', '9876543213', 'Lecturer', 2, 'B.E. (ECE)', '2019-07-01'),
('FAC005', 'Mrs. Anjali Mishra', 'anjali.m@gwpc.edu.in', '9876543214', 'HOD & Lecturer', 3, 'M.Tech (Civil)', '2016-07-01');

-- Students
INSERT INTO students (enrollment_no, full_name, email, phone, dob, department_id, semester, year_of_admission) VALUES
('GWPC2024001', 'Priya Rajput', 'priya.r@student.gwpc.edu.in', '9123456701', '2006-03-15', 1, 1, 2024),
('GWPC2024002', 'Neha Patel', 'neha.p@student.gwpc.edu.in', '9123456702', '2006-05-20', 1, 1, 2024),
('GWPC2024003', 'Anjali Tiwari', 'anjali.t@student.gwpc.edu.in', '9123456703', '2005-11-08', 2, 3, 2023),
('GWPC2024004', 'Kavya Singh', 'kavya.s@student.gwpc.edu.in', '9123456704', '2006-01-25', 3, 1, 2024),
('GWPC2024005', 'Riya Sharma', 'riya.sh@student.gwpc.edu.in', '9123456705', '2005-07-12', 1, 3, 2023),
('GWPC2024006', 'Divya Gupta', 'divya.g@student.gwpc.edu.in', '9123456706', '2004-09-30', 2, 5, 2022),
('GWPC2024007', 'Anika Jain', 'anika.j@student.gwpc.edu.in', '9123456707', '2006-02-14', 4, 1, 2024),
('GWPC2024008', 'Shreya Verma', 'shreya.v@student.gwpc.edu.in', '9123456708', '2005-08-22', 5, 3, 2023);

-- Courses
INSERT INTO courses (name, code, department_id, faculty_id, semester, credits) VALUES
('Programming in C', 'CSE101', 1, 1, 1, 4),
('Data Structures', 'CSE201', 1, 2, 3, 4),
('Digital Electronics', 'ECE101', 2, 3, 1, 3),
('Microprocessors', 'ECE301', 2, 4, 5, 4),
('Surveying', 'CE101', 3, 5, 1, 3),
('Engineering Mathematics', 'MATH101', 1, 1, 1, 4),
('English Communication', 'HUM101', 1, 2, 1, 2),
('Workshop Practice', 'ME101', 4, NULL, 1, 2);

-- Sample Notices
INSERT INTO notices (title, content, category, posted_by, expiry_date) VALUES
('Welcome to New Academic Session 2024-25', 'Dear students, we welcome you to the new academic session. Classes will commence from July 15, 2024. Please collect your timetables from respective departments.', 'academic', 1, '2024-08-01'),
('Mid-Term Examination Schedule', 'Mid-term examinations will be held from August 20-28, 2024. Detailed schedule will be provided by department heads. Students are advised to prepare accordingly.', 'exam', 1, '2024-08-30'),
('Republic Day Celebration', 'Republic Day celebrations will be held on January 26th at 9:00 AM in the college campus. All students and staff are requested to attend.', 'event', 2, '2025-01-27');

-- Sample Attendance
INSERT INTO attendance (student_id, course_id, date, status) VALUES
(1, 1, CURDATE(), 'present'),
(2, 1, CURDATE(), 'present'),
(3, 2, CURDATE(), 'absent'),
(5, 2, CURDATE(), 'present');

-- Sample Marks
INSERT INTO marks (student_id, course_id, exam_type, marks_obtained, max_marks, semester) VALUES
(1, 1, 'internal1', 42, 50, 1),
(2, 1, 'internal1', 38, 50, 1),
(5, 2, 'internal1', 45, 50, 3),
(3, 2, 'internal2', 40, 50, 3);

SELECT 'Database setup complete!' as Status;
