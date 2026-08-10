# app.py - Main Python Flask Web Application with Smart Resilient Login Matching
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
import hashlib
from ai_engine import analyze_student, run_java_report, get_student_ai_chat_response
from database_mysql import load_db_from_mysql, is_mysql_available

app = Flask(__name__)
app.secret_key = 'edupulse_secret_key_123'
DB_PATH = os.path.join(os.path.dirname(__file__), 'database.json')

def hash_password(password):
    """Generates SHA-256 hex digest for passwords."""
    return hashlib.sha256(str(password).strip().encode('utf-8')).hexdigest()

def check_password_match(input_pass, stored_pass):
    """Smart password verification: matches SHA-256 hash or fallback plain text."""
    if not stored_pass:
        return False
    input_str = str(input_pass).strip()
    stored_str = str(stored_pass).strip()
    hashed_input = hash_password(input_str)

    # 1. Compare SHA-256 hash
    if hashed_input == stored_str or hashed_input.lower() == stored_str.lower():
        return True

    # 2. Compare plain text (fallback for older DBs)
    if input_str == stored_str or input_str.lower() == stored_str.lower():
        return True

    return False

def load_db():
    mysql_db = load_db_from_mysql()
    if mysql_db:
        return mysql_db

    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as f:
            data = json.load(f)
            data['source'] = 'JSON_FILE'
            return data
    return {'source': 'JSON_FILE'}

def save_db(data):
    if data.get('source') == 'JSON_FILE':
        with open(DB_PATH, 'w') as f:
            json.dump(data, f, indent=2)

@app.route('/')
def index():
    if 'role' in session:
        role = session['role']
        if role == 'ADMINISTRATOR':
            return redirect(url_for('admin_overview'))
        elif role == 'TEACHER':
            return redirect(url_for('teacher_overview'))
        elif role == 'STUDENT':
            return redirect(url_for('student_performance'))
        elif role == 'PARENT':
            return redirect(url_for('parent_performance'))
    return redirect(url_for('login'))

# LOGIN ROUTE (Resilient Matching across hashed and plain text DBs)
@app.route('/login', methods=['GET', 'POST'])
def login():
    db = load_db()
    if request.method == 'POST':
        user_id_input = str(request.form.get('user_id', '')).strip().lower()
        password_input = str(request.form.get('password', '')).strip()

        # 1. Check Students list
        for s in db.get('students', []):
            s_id = str(s.get('studentId', '')).strip().lower()
            s_email = str(s.get('email', '')).strip().lower()
            stored_pass = str(s.get('password', '')).strip()

            if (user_id_input == s_id or user_id_input == s_email) and check_password_match(password_input, stored_pass):
                session['user_id'] = s['id']
                session['user_name'] = s['name']
                session['role'] = 'STUDENT'
                return redirect(url_for('student_performance'))

        # 2. Check Users list (Admin, Teacher, Parent)
        for u in db.get('users', []):
            u_id = str(u.get('id', '')).strip().lower()
            u_email = str(u.get('email', '')).strip().lower()
            u_name = str(u.get('name', '')).strip().lower()
            stored_pass = str(u.get('password', '')).strip()

            if (user_id_input == u_id or user_id_input == u_email or user_id_input in u_name) and check_password_match(password_input, stored_pass):
                session['user_id'] = u['id']
                session['user_name'] = u['name']
                session['role'] = u['role']
                if u['role'] == 'ADMINISTRATOR':
                    return redirect(url_for('admin_overview'))
                elif u['role'] == 'TEACHER':
                    return redirect(url_for('teacher_overview'))
                elif u['role'] == 'PARENT':
                    return redirect(url_for('parent_performance'))

        return render_template('login.html', error="Invalid Student ID/Email or Password.", db_source=db.get('source'))

    return render_template('login.html', db_source=db.get('source'))

# LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# AI CHATBOT API ROUTE FOR STUDENTS
@app.route('/api/student_chat', methods=['POST'])
def student_chat_api():
    data = request.get_json() or {}
    query = data.get('query', '')
    
    db = load_db()
    student_id = session.get('user_id', 'u3')
    student = next((s for s in db.get('students', []) if s['id'] == student_id), db.get('students', [])[0])

    reply = get_student_ai_chat_response(query, student)
    return jsonify({"reply": reply})

# ========================================================
# 1. ADMIN ROUTES
# ========================================================
@app.route('/admin')
@app.route('/admin/overview')
def admin_overview():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))
    db = load_db()
    teachers = [u for u in db.get('users', []) if u.get('role') == 'TEACHER']
    students = db.get('students', [])
    timetable = db.get('timetable', [])
    return render_template('admin.html', active_role='ADMINISTRATOR', active_sub='overview', user_name=session.get('user_name'), teachers=teachers, students=students, timetable=timetable, db_source=db.get('source'))

@app.route('/admin/teachers')
def admin_teachers():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))
    db = load_db()
    teachers = [u for u in db.get('users', []) if u.get('role') == 'TEACHER']
    return render_template('admin.html', active_role='ADMINISTRATOR', active_sub='teachers', user_name=session.get('user_name'), teachers=teachers, db_source=db.get('source'))

@app.route('/admin/students')
def admin_students():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))
    db = load_db()
    students = db.get('students', [])
    return render_template('admin.html', active_role='ADMINISTRATOR', active_sub='students', user_name=session.get('user_name'), students=students, db_source=db.get('source'))

@app.route('/admin/parents')
def admin_parents():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))
    db = load_db()
    parents = [u for u in db.get('users', []) if u.get('role') == 'PARENT']
    return render_template('admin.html', active_role='ADMINISTRATOR', active_sub='parents', user_name=session.get('user_name'), parents=parents, db_source=db.get('source'))

@app.route('/admin/timetable')
def admin_timetable():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))
    db = load_db()
    timetable = db.get('timetable', [])
    return render_template('admin.html', active_role='ADMINISTRATOR', active_sub='timetable', user_name=session.get('user_name'), timetable=timetable, db_source=db.get('source'))

@app.route('/admin/add_teacher', methods=['POST'])
def add_teacher():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))

    db = load_db()
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')

    new_t = {
        "id": f"u_{len(db.get('users', [])) + 1}",
        "name": name,
        "role": "TEACHER",
        "email": email,
        "password": hash_password("teacher123"),
        "subject": subject,
        "class": "Class 10-A"
    }

    db['users'].append(new_t)
    save_db(db)
    return redirect(url_for('admin_teachers'))

@app.route('/admin/add_student', methods=['POST'])
def add_student():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))

    db = load_db()
    name = request.form.get('name')
    s_id = request.form.get('student_id')

    new_s = {
        "id": f"s_{len(db.get('students', [])) + 1}",
        "name": name,
        "studentId": s_id,
        "password": hash_password("student123"),
        "class": "Class 10-A",
        "attendance": 90,
        "parentName": "Parent Pending",
        "marks": { "Physics": 75, "Maths": 75, "Chemistry": 75, "ComputerScience": 75 },
        "teacherRemarks": "Newly enrolled student.",
        "quizzes": [],
        "assignments": []
    }

    db['students'].append(new_s)
    save_db(db)
    return redirect(url_for('admin_students'))

@app.route('/admin/add_timetable', methods=['POST'])
def add_timetable():
    if session.get('role') != 'ADMINISTRATOR':
        return redirect(url_for('login'))

    db = load_db()
    day = request.form.get('day')
    time = request.form.get('time')
    subject = request.form.get('subject')
    room = request.form.get('room')

    new_slot = {
        "period": len(db.get('timetable', [])) + 1,
        "day": day,
        "time": time,
        "subject": subject,
        "teacher": "Prof. Sterling",
        "room": room
    }

    db['timetable'].append(new_slot)
    save_db(db)
    return redirect(url_for('admin_timetable'))

# ========================================================
# 2. TEACHER ROUTES
# ========================================================
def get_teacher_data():
    db = load_db()
    students = db.get('students', [])
    student_ai_list = []
    for s in students:
        ai_res = analyze_student(s)
        student_ai_list.append({"student": s, "ai": ai_res})
    return db, students, student_ai_list

@app.route('/teacher')
@app.route('/teacher/overview')
def teacher_overview():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, students, student_ai_list = get_teacher_data()
    return render_template('teacher.html', active_role='TEACHER', active_sub='overview', user_name=session.get('user_name'), students=students, student_ai_list=student_ai_list, db_source=db.get('source'))

@app.route('/teacher/marks')
def teacher_marks():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, students, student_ai_list = get_teacher_data()
    return render_template('teacher.html', active_role='TEACHER', active_sub='marks', user_name=session.get('user_name'), students=students, student_ai_list=student_ai_list, db_source=db.get('source'))

@app.route('/teacher/attendance')
def teacher_attendance():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, students, student_ai_list = get_teacher_data()
    return render_template('teacher.html', active_role='TEACHER', active_sub='attendance', user_name=session.get('user_name'), students=students, student_ai_list=student_ai_list, db_source=db.get('source'))

@app.route('/teacher/assignments')
def teacher_assignments():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, students, student_ai_list = get_teacher_data()
    return render_template('teacher.html', active_role='TEACHER', active_sub='assignments', user_name=session.get('user_name'), students=students, student_ai_list=student_ai_list, db_source=db.get('source'))

@app.route('/teacher/quizzes')
def teacher_quizzes():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, students, student_ai_list = get_teacher_data()
    return render_template('teacher.html', active_role='TEACHER', active_sub='quizzes', user_name=session.get('user_name'), students=students, student_ai_list=student_ai_list, db_source=db.get('source'))

@app.route('/teacher/records')
def teacher_records():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, students, student_ai_list = get_teacher_data()
    return render_template('teacher.html', active_role='TEACHER', active_sub='records', user_name=session.get('user_name'), students=students, student_ai_list=student_ai_list, db_source=db.get('source'))

@app.route('/teacher/update_marks', methods=['POST'])
def update_marks():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))

    db = load_db()
    student_id = request.form.get('student_id')
    physics = int(request.form.get('physics', 0))
    maths = int(request.form.get('maths', 0))
    chemistry = int(request.form.get('chemistry', 0))
    cs = int(request.form.get('cs', 0))

    for s in db.get('students', []):
        if s['id'] == student_id:
            s['marks'] = {
                "Physics": physics,
                "Maths": maths,
                "Chemistry": chemistry,
                "ComputerScience": cs
            }
            break

    save_db(db)
    return redirect(url_for('teacher_marks'))

@app.route('/teacher/update_attendance', methods=['POST'])
def update_attendance():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))

    db = load_db()
    student_id = request.form.get('student_id')
    attendance = int(request.form.get('attendance', 90))

    for s in db.get('students', []):
        if s['id'] == student_id:
            s['attendance'] = min(100, attendance)
            break

    save_db(db)
    return redirect(url_for('teacher_attendance'))

@app.route('/teacher/add_assignment', methods=['POST'])
def add_assignment():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))

    db = load_db()
    title = request.form.get('title')
    due_date = request.form.get('dueDate')

    new_asg = {
        "title": title,
        "subject": "Physics",
        "dueDate": due_date,
        "status": "Assigned",
        "grade": "Pending"
    }

    for s in db.get('students', []):
        if 'assignments' not in s:
            s['assignments'] = []
        s['assignments'].append(new_asg)

    save_db(db)
    return redirect(url_for('teacher_assignments'))

@app.route('/teacher/add_quiz', methods=['POST'])
def add_quiz():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))

    db = load_db()
    title = request.form.get('title')
    
    new_q = {
        "title": title,
        "score": 75,
        "total": 100,
        "date": "2026-08-10"
    }

    for s in db.get('students', []):
        if 'quizzes' not in s:
            s['quizzes'] = []
        s['quizzes'].append(new_q)

    save_db(db)
    return redirect(url_for('teacher_quizzes'))

@app.route('/teacher/add_remark', methods=['POST'])
def add_remark():
    if session.get('role') not in ['TEACHER', 'ADMINISTRATOR']:
        return redirect(url_for('login'))

    db = load_db()
    student_id = request.form.get('student_id')
    remark = request.form.get('remark')

    for s in db.get('students', []):
        if s['id'] == student_id:
            s['teacherRemarks'] = remark
            break

    save_db(db)
    return redirect(url_for('teacher_records'))

# ========================================================
# 3. STUDENT ROUTES
# ========================================================
def get_student_data():
    db = load_db()
    student_id = session.get('user_id', 'u3')
    student = next((s for s in db.get('students', []) if s['id'] == student_id), db.get('students', [])[0])
    ai = analyze_student(student)
    timetable = db.get('timetable', [])
    return db, student, ai, timetable

@app.route('/student')
@app.route('/student/performance')
def student_performance():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='performance', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/student/marks')
def student_marks():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='marks', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/student/attendance')
def student_attendance():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='attendance', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/student/assignments')
def student_assignments():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='assignments', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/student/quizzes')
def student_quizzes():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='quizzes', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/student/remarks')
def student_remarks():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='remarks', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/student/timetable')
def student_timetable():
    if session.get('role') not in ['STUDENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, student, ai, timetable = get_student_data()
    return render_template('student.html', active_role='STUDENT', active_sub='timetable', user_name=session.get('user_name'), student=student, ai=ai, timetable=timetable, db_source=db.get('source'))

# ========================================================
# 4. PARENT ROUTES
# ========================================================
def get_parent_data():
    db = load_db()
    parent_id = session.get('user_id', 'u5')
    parent = next((u for u in db.get('users', []) if u.get('id') == parent_id and u.get('role') == 'PARENT'), [u for u in db.get('users', []) if u.get('role') == 'PARENT'][0])
    child = next((s for s in db.get('students', []) if s['id'] == parent.get('childId')), db.get('students', [])[0])
    ai = analyze_student(child)
    timetable = db.get('timetable', [])
    return db, parent, child, ai, timetable

@app.route('/parent')
@app.route('/parent/performance')
def parent_performance():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='performance', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/profile')
def parent_profile():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='profile', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/marks')
def parent_marks():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='marks', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/attendance')
def parent_attendance():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='attendance', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/assignments')
def parent_assignments():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='assignments', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/quizzes')
def parent_quizzes():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='quizzes', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/remarks')
def parent_remarks():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='remarks', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

@app.route('/parent/timetable')
def parent_timetable():
    if session.get('role') not in ['PARENT', 'ADMINISTRATOR']:
        return redirect(url_for('login'))
    db, parent, child, ai, timetable = get_parent_data()
    return render_template('parent.html', active_role='PARENT', active_sub='timetable', user_name=session.get('user_name'), parent=parent, child=child, ai=ai, timetable=timetable, db_source=db.get('source'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
