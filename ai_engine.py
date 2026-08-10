# ai_engine.py - Python AI Analysis & Chatbot Engine
import os
import subprocess
import json

def run_c_gpa_calculator(physics, maths, chemistry, comp_sci, attendance):
    c_exe = os.path.join(os.path.dirname(__file__), 'c_engine', 'gpa_calculator.exe')
    if os.path.exists(c_exe):
        try:
            cmd = [c_exe, str(physics), str(maths), str(chemistry), str(comp_sci), str(attendance)]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if res.returncode == 0:
                data = json.loads(res.stdout.strip())
                return data
        except Exception as e:
            print(f"C engine execution fallback: {e}")

    avg = (physics + maths + chemistry + comp_sci) / 4.0
    gpa = (avg / 100.0) * 4.0
    risk = 2 if (avg < 60 or attendance < 75) else (1 if (avg < 75 or attendance < 85) else 0)
    return {"average": round(avg, 2), "gpa": round(gpa, 2), "risk_flag": risk}

def analyze_student(student):
    marks = student.get('marks', {})
    physics = marks.get('Physics', 0)
    maths = marks.get('Maths', 0)
    chem = marks.get('Chemistry', 0)
    cs = marks.get('ComputerScience', 0)
    attendance = student.get('attendance', 0)

    c_result = run_c_gpa_calculator(physics, maths, chem, cs, attendance)
    avg_score = c_result['average']
    gpa = c_result['gpa']
    risk_flag = c_result['risk_flag']

    if risk_flag == 2:
        status = "Needs Additional Support"
        risk_badge = "danger"
        recommendation = f"AI Recommendation: {student['name']} requires targeted tutoring in lower scoring subjects. Recommend morning attendance tracking."
        parent_tip = f"Parent Tip: Review {student['name']}'s evening study routine and focus on Physics revision."
    elif risk_flag == 1:
        status = "Moderate / Average"
        risk_badge = "warning"
        recommendation = f"AI Recommendation: {student['name']} has steady performance. Focus on consistent assignment submission."
        parent_tip = f"Parent Tip: Check weekly quiz scores."
    else:
        status = "Excellent Standing"
        risk_badge = "success"
        recommendation = f"AI Recommendation: {student['name']} is excelling! Recommend advanced STEM competitions and peer tutoring."
        parent_tip = f"Parent Tip: Encourage participation in science Olympiads."

    return {
        "average_score": avg_score,
        "gpa": gpa,
        "status": status,
        "risk_badge": risk_badge,
        "recommendation": recommendation,
        "parent_tip": parent_tip
    }

def run_java_report(name, student_id, student_class, gpa, attendance):
    java_class = os.path.join(os.path.dirname(__file__), 'java_engine')
    try:
        cmd = ["java", "-cp", java_class, "ReportGenerator", name, student_id, student_class, str(gpa), str(attendance)]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
        if res.returncode == 0:
            return res.stdout
    except Exception as e:
        print(f"Java report generator fallback: {e}")

    return f"Report Card for {name} ({student_id}) - GPA: {gpa}, Attendance: {attendance}%"

def get_student_ai_chat_response(query, student):
    """
    AI Chatbot Engine processing student natural language queries
    using student's live academic context (marks, attendance, remarks).
    """
    q = query.lower().strip()
    marks = student.get('marks', {})
    physics = marks.get('Physics', 0)
    maths = marks.get('Maths', 0)
    chem = marks.get('Chemistry', 0)
    cs = marks.get('ComputerScience', 0)
    attendance = student.get('attendance', 0)
    name = student.get('name', 'Student')

    # Subject-specific recommendations
    if 'physics' in q:
        return f"💡 **AI Advice for Physics (Current Score: {physics}%):**\n" \
               f"To improve Physics, focus 45 mins daily on Newton's Laws and Kinematics numerical problems. " \
               f"Review your Physics Quiz 1 solutions and complete 10 practice problems before Friday."

    if 'math' in q or 'calculus' in q:
        return f"💡 **AI Advice for Maths (Current Score: {maths}%):**\n" \
               f"Maths requires step-by-step problem set practice. Practice integration and algebra equations " \
               f"for 30 minutes every evening. Ask Prof. Sterling for the remedial problem sheet."

    if 'computer' in q or 'coding' in q or 'cs' in q:
        return f"🌟 **AI Feedback for Computer Science (Current Score: {cs}%):**\n" \
               f"You are doing fantastic in Computer Science ({cs}%)! Keep building your python & algorithm projects. " \
               f"Consider peer mentoring classmates who need help in coding."

    if 'schedule' in q or 'routine' in q or 'plan' in q or 'timetable' in q:
        return f"📅 **AI Recommended Weekly Study Plan for {name}:**\n" \
               f"• Monday & Wednesday (4:00 - 5:30 PM): Physics Problem Sets & Formula Review\n" \
               f"• Tuesday & Thursday (4:00 - 5:00 PM): Maths & Calculus Practice\n" \
               f"• Friday (4:00 - 5:00 PM): Chemistry Reactions & Lab Report Review\n" \
               f"• Saturday: Take 1 Mock Quiz (30 mins)"

    if 'attendance' in q or 'absent' in q:
        if attendance < 75:
            return f"⚠️ **AI Attendance Warning (Current: {attendance}%):**\n" \
                   f"Your attendance is below the 75% requirement. Set 2 morning alarm reminders and attend all " \
                   f"Monday and Tuesday morning classes to recover your attendance standing!"
        else:
            return f"✅ **Attendance Standing (Current: {attendance}%):**\n" \
                   f"Your attendance is in good standing! Keep maintaining regular punctuality."

    if 'gpa' in q or 'improve' in q or 'score' in q or 'help' in q:
        lowest_sub = min(marks, key=marks.get) if marks else 'Physics'
        lowest_score = marks.get(lowest_sub, 0)
        return f"🎯 **AI Overall Performance Strategy for {name}:**\n" \
               f"Your lowest scoring subject right now is **{lowest_sub} ({lowest_score}%)**. " \
               f"Raising this score by 15% will boost your overall GPA above 3.5! " \
               f"Focus on {lowest_sub} study sets this week."

    # General AI assistant reply
    return f"🤖 **AI Study Advisor:** Hi {name}! I analyzed your grades (Physics: {physics}%, Maths: {maths}%, CS: {cs}%). " \
           f"You can ask me questions like:\n" \
           f"• 'How can I improve my Physics score?'\n" \
           f"• 'Give me a weekly study schedule'\n" \
           f"• 'How to raise my overall GPA?'"
