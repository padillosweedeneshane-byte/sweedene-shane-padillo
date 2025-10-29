from flask import Flask, render_template_string, request, redirect, url_for, session
import random, json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

DATA_FILE = "students.json"
LOG_FILE = "login_log.json"

def load_students():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_students():
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=4)

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(login_logs, f, indent=4)

students = load_students()
login_logs = load_logs()

sections = ["Levi", "Reuben", "Zechariah", "Judah", "Benjamin", "Asher", "Dan", "Simeon"]

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        grade = request.form['grade'].strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        if name.lower() == "admin" and grade == "0000":
            session.clear()
            session["admin"] = True
            login_logs.append({"name": "Admin", "role": "Admin", "time": timestamp})
            save_logs()
            return redirect(url_for('admin_dashboard'))

        student = next((s for s in students if s["name"].lower() == name.lower()), None)

        if not student:
            new_id = len(students) + 1
            random_section = random.choice(sections)
            student = {"id": new_id, "name": name, "grade": grade, "section": random_section}
            students.append(student)
            save_students()

        session.clear()
        session["student"] = student
        login_logs.append({"name": name, "role": "Student", "time": timestamp})
        save_logs()
        return redirect(url_for('student_dashboard'))

    return render_template_string(login_page)

@app.route('/student/dashboard')
def student_dashboard():
    if "student" not in session:
        return redirect(url_for('login'))
    student = session["student"]
    now = datetime.now().strftime("%B %d, %Y %I:%M %p")
    return render_template_string(student_dashboard_page, student=student, now=now)

@app.route('/admin')
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for('login'))
    now = datetime.now().strftime("%B %d, %Y %I:%M %p")
    return render_template_string(admin_page, students=students, logs=login_logs, now=now)

@app.route('/admin/add', methods=['POST'])
def add_student():
    if "admin" not in session:
        return redirect(url_for('login'))
    name = request.form['name']
    grade = request.form['grade']
    section = request.form['section']
    new_id = len(students) + 1
    students.append({"id": new_id, "name": name, "grade": grade, "section": section})
    save_students()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if "admin" not in session:
        return redirect(url_for('login'))
    student = next((s for s in students if s["id"] == id), None)
    if not student:
        return "Student not found", 404

    if request.method == 'POST':
        student["name"] = request.form['name']
        student["grade"] = request.form['grade']
        student["section"] = request.form['section']
        save_students()
        return redirect(url_for('admin_dashboard'))

    return render_template_string(edit_page, student=student)

@app.route('/admin/delete/<int:id>')
def delete_student(id):
    if "admin" not in session:
        return redirect(url_for('login'))
    global students
    students = [s for s in students if s["id"] != id]
    save_students()
    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ========== HTML Templates ==========

login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #ffe0eb, #fff7fa);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            transition: background 1s;
        }
        .box {
            background: #fff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            text-align: center;
            width: 350px;
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
        }
        h1 { color: #e91e63; }
        input {
            width: 90%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            transition: background 0.5s;
        }
        button:hover { background: #c2185b; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Login</h1>
        <form method="POST">
            <input type="text" name="name" placeholder="Name (Admin or Student)" required><br>
            <input type="text" name="grade" placeholder="Grade (or 0000 for Admin)" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

student_dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Dashboard</title>
    <style>
        :root {
            --bg: #fdf2f7;
            --text: #000;
            --card: #fff;
            --accent: #e91e63;
        }
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg);
            color: var(--text);
            text-align: center;
            padding: 50px;
            transition: all 1s ease;
        }
        .card {
            background: var(--card);
            color: var(--text);
            padding: 30px 50px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            display: inline-block;
            animation: fadeIn 1.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
        h1 { color: var(--accent); transition: color 1s ease; }
        button {
            background: var(--accent);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            transition: background 1s ease;
        }
        .dark-toggle {
            position: fixed;
            top: 20px; right: 20px;
            background: #555;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 5px 10px;
            cursor: pointer;
            animation: glow 3s ease-in-out infinite;
        }
        @keyframes glow {
            0%,100% { box-shadow: 0 0 10px #e91e63; }
            50% { box-shadow: 0 0 20px #ff80ab; }
        }
    </style>
</head>
<body>
    <button class="dark-toggle" onclick="toggleDark()">🌙</button>
    <h1>🎓 Welcome, {{ student.name }}!</h1>
    <p>{{ now }}</p>
    <div class="card">
        <p><strong>ID:</strong> {{ student.id }}</p>
        <p><strong>Grade:</strong> {{ student.grade }}</p>
        <p><strong>Section:</strong> {{ student.section }}</p>
        <p>✨ Keep learning and doing great!</p>
        <a href="{{ url_for('logout') }}"><button>Logout</button></a>
    </div>

    <script>
        let dark = false;
        function toggleDark() {
            dark = !dark;
            document.documentElement.style.setProperty('--bg', dark ? '#111' : '#fdf2f7');
            document.documentElement.style.setProperty('--text', dark ? '#fff' : '#000');
            document.documentElement.style.setProperty('--card', dark ? '#222' : '#fff');
            document.documentElement.style.setProperty('--accent', dark ? '#ff80ab' : '#e91e63');
        }
    </script>
</body>
</html>
"""

admin_page = student_dashboard_page.replace("Student Dashboard", "Admin Dashboard").replace("🎓 Welcome, {{ student.name }}!", "👩‍🏫 Admin Dashboard").replace("{{ student.id }}", "").replace("{{ student.grade }}", "").replace("{{ student.section }}", "")

edit_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Edit Student</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: #fdf2f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: #fff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            text-align: center;
            animation: fadeIn 2s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        h1 { color: #e91e63; }
        input {
            padding: 10px;
            width: 90%;
            margin: 10px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            transition: background 1s ease;
        }
        button:hover { background: #ff80ab; }
    </style>
</head>
<body>
    <div class="box">
        <h1>Edit Student</h1>
        <form method="POST">
            <input type="text" name="name" value="{{ student.name }}" required><br>
            <input type="text" name="grade" value="{{ student.grade }}" required><br>
            <input type="text" name="section" value="{{ student.section }}" required><br>
            <button type="submit">Save Changes</button>
        </form>
        <br>
        <a href="{{ url_for('admin_dashboard') }}"><button>Back</button></a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
