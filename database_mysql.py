# database_mysql.py - Python XAMPP MySQL Connector
import pymysql

MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'student_db',
    'cursorclass': pymysql.cursors.DictCursor,
    'connect_timeout': 3
}

def is_mysql_available():
    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        conn.close()
        return True
    except Exception as e:
        return False

def load_db_from_mysql():
    if not is_mysql_available():
        return None

    try:
        conn = pymysql.connect(**MYSQL_CONFIG)
        cursor = conn.cursor()

        # 1. Fetch Users
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        # 2. Fetch Students
        cursor.execute("SELECT * FROM students")
        raw_students = cursor.fetchall()

        students = []
        for s in raw_students:
            # Fetch Marks
            cursor.execute("SELECT physics, maths, chemistry, computer_science FROM marks WHERE student_id = %s", (s['id'],))
            m = cursor.fetchone() or {"physics": 75, "maths": 75, "chemistry": 75, "computer_science": 75}

            # Fetch Quizzes
            cursor.execute("SELECT title, score, total, DATE_FORMAT(date, '%%Y-%%m-%%d') as date FROM quizzes")
            quizzes = cursor.fetchall()

            student_obj = {
                "id": s['id'],
                "name": s['name'],
                "studentId": s['student_id'],
                "password": s['password'],
                "class": s['class'],
                "attendance": s['attendance'],
                "parentName": s['parent_name'],
                "teacherRemarks": s['teacher_remarks'],
                "marks": {
                    "Physics": m['physics'],
                    "Maths": m['maths'],
                    "Chemistry": m['chemistry'],
                    "ComputerScience": m['computer_science']
                },
                "quizzes": quizzes,
                "assignments": [
                    { "title": "Lab Report 1: Rotational Motion", "subject": "Physics", "dueDate": "2026-08-15", "status": "Submitted", "grade": "82/100" },
                    { "title": "Calculus Integration Set", "subject": "Maths", "dueDate": "2026-08-18", "status": "Pending", "grade": "Pending" }
                ]
            }
            students.append(student_obj)

        # 3. Fetch Timetable (Ordered by Day & Period)
        cursor.execute("SELECT id, period, day, time, subject, teacher, room FROM timetable ORDER BY FIELD(day, 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'), period, id")
        timetable = cursor.fetchall()

        conn.close()

        return {
            "users": users,
            "students": students,
            "timetable": timetable,
            "source": "XAMPP_MYSQL"
        }
    except Exception as e:
        print(f"MySQL error: {e}")
        return None
