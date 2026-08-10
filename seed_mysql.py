# seed_mysql.py - Automates inserting all updated schemas with SHA-256 Password Hashes into XAMPP MySQL
import pymysql
import hashlib

def hash_pw(pw):
    return hashlib.sha256(str(pw).strip().encode('utf-8')).hexdigest()

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'cursorclass': pymysql.cursors.DictCursor
}

def seed_xampp_mysql():
    print("Connecting to XAMPP MySQL...")
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # 1. Create Database
        cursor.execute("CREATE DATABASE IF NOT EXISTS `student_db`;")
        cursor.execute("USE `student_db`;")

        # 2. Re-create Tables
        cursor.execute("DROP TABLE IF EXISTS `marks`;")
        cursor.execute("DROP TABLE IF EXISTS `quizzes`;")
        cursor.execute("DROP TABLE IF EXISTS `timetable`;")
        cursor.execute("DROP TABLE IF EXISTS `students`;")
        cursor.execute("DROP TABLE IF EXISTS `users`;")

        cursor.execute("""
        CREATE TABLE `users` (
          `id` VARCHAR(50) PRIMARY KEY,
          `name` VARCHAR(100) NOT NULL,
          `role` VARCHAR(20) NOT NULL,
          `email` VARCHAR(100) NOT NULL,
          `password` VARCHAR(100) NOT NULL,
          `subject` VARCHAR(100) DEFAULT NULL,
          `class` VARCHAR(50) DEFAULT NULL,
          `phone` VARCHAR(50) DEFAULT NULL,
          `child_id` VARCHAR(50) DEFAULT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE `students` (
          `id` VARCHAR(50) PRIMARY KEY,
          `name` VARCHAR(100) NOT NULL,
          `student_id` VARCHAR(50) NOT NULL,
          `password` VARCHAR(100) NOT NULL,
          `class` VARCHAR(50) NOT NULL,
          `attendance` INT DEFAULT 90,
          `parent_name` VARCHAR(100) DEFAULT NULL,
          `teacher_remarks` TEXT DEFAULT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE `marks` (
          `id` INT AUTO_INCREMENT PRIMARY KEY,
          `student_id` VARCHAR(50) NOT NULL,
          `physics` INT DEFAULT 75,
          `maths` INT DEFAULT 75,
          `chemistry` INT DEFAULT 75,
          `computer_science` INT DEFAULT 75,
          `english` INT DEFAULT 85,
          `biology` INT DEFAULT 72,
          `env_science` INT DEFAULT 88,
          `physical_edu` INT DEFAULT 95,
          FOREIGN KEY (`student_id`) REFERENCES `students`(`id`) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
        CREATE TABLE `timetable` (
          `id` INT AUTO_INCREMENT PRIMARY KEY,
          `period` INT NOT NULL,
          `day` VARCHAR(20) NOT NULL,
          `time` VARCHAR(50) NOT NULL,
          `subject` VARCHAR(100) NOT NULL,
          `teacher` VARCHAR(100) NOT NULL,
          `room` VARCHAR(50) NOT NULL
        );
        """)

        cursor.execute("""
        CREATE TABLE `quizzes` (
          `id` INT AUTO_INCREMENT PRIMARY KEY,
          `title` VARCHAR(100) NOT NULL,
          `subject` VARCHAR(50) DEFAULT 'Physics',
          `score` INT DEFAULT 75,
          `total` INT DEFAULT 100,
          `date` DATE NOT NULL
        );
        """)

        # 3. Seed Users with SHA-256 Password Hashes
        admin_hash = hash_pw('admin123')
        teacher_hash = hash_pw('teacher123')
        student_hash = hash_pw('student123')
        parent_hash = hash_pw('parent123')

        cursor.execute("""
        INSERT INTO `users` (`id`, `name`, `role`, `email`, `password`, `subject`, `class`, `phone`, `child_id`) VALUES
        ('u1', 'Dr. Sarah Vance', 'ADMINISTRATOR', 'admin@school.com', %s, NULL, NULL, NULL, NULL),
        ('u2', 'Prof. Marcus Sterling', 'TEACHER', 'teacher@school.com', %s, 'Physics & Math', 'Class 10-A', NULL, NULL),
        ('u3', 'Alex Rivera', 'STUDENT', 'alex@student.com', %s, NULL, 'Class 10-A', NULL, NULL),
        ('u4', 'Sophia Chen', 'STUDENT', 'sophia@student.com', %s, NULL, 'Class 10-A', NULL, NULL),
        ('u5', 'Robert Rivera', 'PARENT', 'robert@parent.com', %s, NULL, NULL, '+1 555-0192', 'u3');
        """, (admin_hash, teacher_hash, student_hash, student_hash, parent_hash))

        # 4. Seed Students & Marks
        cursor.execute("""
        INSERT INTO `students` (`id`, `name`, `student_id`, `password`, `class`, `attendance`, `parent_name`, `teacher_remarks`) VALUES
        ('u3', 'Alex Rivera', 'STU-101', %s, 'Class 10-A', 72, 'Robert Rivera', 'Alex is doing great in Computer Science, but needs extra practice in Physics.'),
        ('u4', 'Sophia Chen', 'STU-102', %s, 'Class 10-A', 98, 'Jennifer Chen', 'Outstanding academic performance and class leadership.');
        """, (student_hash, student_hash))

        cursor.execute("""
        INSERT INTO `marks` (`student_id`, `physics`, `maths`, `chemistry`, `computer_science`, `english`, `biology`, `env_science`, `physical_edu`) VALUES
        ('u3', 58, 62, 78, 94, 85, 72, 88, 95),
        ('u4', 96, 98, 94, 100, 92, 95, 94, 98);
        """)

        # 5. Seed 40-Period 8-Subject Timetable
        cursor.execute("""
        INSERT INTO `timetable` (`period`, `day`, `time`, `subject`, `teacher`, `room`) VALUES
        (1, 'Monday', '08:30 AM - 09:15 AM', 'Physics', 'kamal mam', 'Lab 1'),
        (2, 'Monday', '09:15 AM - 10:00 AM', 'Maths', 'sunita mam', 'Room 204'),
        (3, 'Monday', '10:00 AM - 10:45 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
        (4, 'Monday', '10:45 AM - 11:30 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
        (5, 'Monday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
        (6, 'Monday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
        (7, 'Monday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
        (8, 'Monday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground'),

        (1, 'Tuesday', '08:30 AM - 09:15 AM', 'Maths', 'sunita mam', 'Room 204'),
        (2, 'Tuesday', '09:15 AM - 10:00 AM', 'Physics', 'kamal mam', 'Lab 1'),
        (3, 'Tuesday', '10:00 AM - 10:45 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
        (4, 'Tuesday', '10:45 AM - 11:30 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
        (5, 'Tuesday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
        (6, 'Tuesday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
        (7, 'Tuesday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
        (8, 'Tuesday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground'),

        (1, 'Wednesday', '08:30 AM - 09:15 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
        (2, 'Wednesday', '09:15 AM - 10:00 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
        (3, 'Wednesday', '10:00 AM - 10:45 AM', 'Physics Lab', 'ankur sir', 'Lab 1'),
        (4, 'Wednesday', '10:45 AM - 11:30 AM', 'Maths', 'sunita mam', 'Room 204'),
        (5, 'Wednesday', '11:30 AM - 12:15 PM', 'Physics', 'kamal mam', 'Lab 1'),
        (6, 'Wednesday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
        (7, 'Wednesday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
        (8, 'Wednesday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground'),

        (1, 'Thursday', '08:30 AM - 09:15 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
        (2, 'Thursday', '09:15 AM - 10:00 AM', 'English Literature', 'Priya mam', 'Room 101'),
        (3, 'Thursday', '10:00 AM - 10:45 AM', 'Maths', 'sunita mam', 'Room 204'),
        (4, 'Thursday', '10:45 AM - 11:30 AM', 'Physics', 'kamal mam', 'Lab 1'),
        (5, 'Thursday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
        (6, 'Thursday', '01:00 PM - 01:45 PM', 'Chemistry', 'geenu mam', 'Lab 2'),
        (7, 'Thursday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
        (8, 'Thursday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Gym'),

        (1, 'Friday', '08:30 AM - 09:15 AM', 'Physics', 'kamal mam', 'Lab 1'),
        (2, 'Friday', '09:15 AM - 10:00 AM', 'Maths', 'sunita mam', 'Room 204'),
        (3, 'Friday', '10:00 AM - 10:45 AM', 'Chemistry', 'geenu mam', 'Lab 2'),
        (4, 'Friday', '10:45 AM - 11:30 AM', 'Computer Science', 'Ashita mam', 'CompLab A'),
        (5, 'Friday', '11:30 AM - 12:15 PM', 'Physics Lab', 'ankur sir', 'Lab 1'),
        (6, 'Friday', '01:00 PM - 01:45 PM', 'English Literature', 'Priya mam', 'Room 101'),
        (7, 'Friday', '01:45 PM - 02:30 PM', 'Biology', 'Ravi sir', 'BioLab'),
        (8, 'Friday', '02:30 PM - 03:15 PM', 'Physical Education', 'Vikram sir', 'Sports Ground');
        """)

        # 6. Seed Quizzes
        cursor.execute("""
        INSERT INTO `quizzes` (`title`, `subject`, `score`, `total`, `date`) VALUES
        ('Physics Quiz 1', 'Physics', 58, 100, '2026-08-01'),
        ('Math Test 1', 'Maths', 64, 100, '2026-07-25');
        """)

        conn.commit()
        conn.close()
        print("Successfully seeded XAMPP MySQL database 'student_db' with SHA-256 hashed passwords!")
        return True
    except Exception as e:
        print(f"XAMPP MySQL connection/seeding error: {e}")
        return False

if __name__ == '__main__':
    seed_xampp_mysql()
