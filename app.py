from flask import Flask, render_template_string, request, redirect, url_for, session
import random, json, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------------------
# Load/Save Students from JSON
# -------------------------------
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

# Possible random sections
sections = ["Levi", "Reuben", "Zechariah", "Judah", "Benjamin", "Asher", "Dan", "Simeon"]

# --------------------------------
# LOGIN PAGE - Anyone can log in
# --------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        grade = request.form['grade'].strip()
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        # Admin login
        if name.lower() == "admin" and grade == "0000":
            session.clear()
            session["admin"] = True
            # Record admin login
            login_logs.append({"name": "Admin", "role": "Admin", "time": timestamp})
            save_logs()
            return redirect(url_for('admin_dashboard'))

        # Check if student already exists
        student = next((s for s in students if s["name"].lower() == name.lower()), None)

        # If not found, register automatically
        if not student:
            new_id = len(students) + 1
            random_section = random.choice(sections)
            student = {"id": new_id, "name": name, "grade": grade, "section": random_section}
            students.append(student)
            save_students()

        # Log in as student
        session.clear()
        session["student"] = student

        # Record student login
        login_logs.append({"name": name, "role": "Student", "time": timestamp})
        save_logs()

        return redirect(url_for('student_dashboard'))

    return render_template_string(login_page)

# --------------------------------
# STUDENT DASHBOARD
# --------------------------------
@app.route('/student/dashboard')
def student_dashboard():
    if "student" not in session:
        return redirect(url_for('login'))
    student = session["student"]
    now = datetime.now().strftime("%B %d, %Y %I:%M %p")
    return render_template_string(student_dashboard_page, student=student, now=now)

# --------------------------------
# ADMIN DASHBOARD
# --------------------------------
@app.route('/admin')
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for('login'))
    now = datetime.now().strftime("%B %d, %Y %I:%M %p")
    return render_template_string(admin_page, students=students, logs=login_logs, now=now)

# Add student manually (Admin)
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

# Edit student
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

# Delete student
@app.route('/admin/delete/<int:id>')
def delete_student(id):
    if "admin" not in session:
        return redirect(url_for('login'))
    global students
    students = [s for s in students if s["id"] != id]
    save_students()
    return redirect(url_for('admin_dashboard'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --------------------------------
# HTML Templates
# --------------------------------

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
        }
        .box {
            background: #fff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            text-align: center;
            width: 350px;
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
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg, #fdf2f7);
            color: var(--text, black);
            text-align: center;
            padding: 50px;
            transition: background 0.5s, color 0.5s;
        }
        .card {
            background: #fff;
            padding: 30px 50px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            display: inline-block;
        }
        h1 { color: #e91e63; }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
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
        <p>✨ Tip: Keep your grades up and check back for updates!</p>
        <a href="{{ url_for('logout') }}"><button>Logout</button></a>
    </div>
    <script>
        function toggleDark() {
            const isDark = document.body.style.getPropertyValue('--bg') === '#111';
            document.body.style.setProperty('--bg', isDark ? '#fdf2f7' : '#111');
            document.body.style.setProperty('--text', isDark ? 'black' : 'white');
        }
    </script>
</body>
</html>
"""

admin_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Admin Dashboard</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--bg, #fff7fa);
            color: var(--text, black);
            padding: 30px;
            transition: background 0.5s, color 0.5s;
        }
        h1 { color: #e91e63; text-align: center; }
        table {
            width: 80%;
            margin: auto;
            border-collapse: collapse;
            background: #fff;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
        }
        th, td {
            border-bottom: 1px solid #f3d1dc;
            padding: 12px;
            text-align: center;
        }
        th { background: #f8c1d2; }
        a, button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 6px 15px;
            border-radius: 15px;
            text-decoration: none;
        }
        form {
            text-align: center;
            margin-top: 30px;
        }
        input {
            padding: 8px;
            margin: 5px;
            border-radius: 10px;
            border: 1px solid #ccc;
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
        }
        h2 {
            text-align: center;
            color: #c2185b;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <button class="dark-toggle" onclick="toggleDark()">🌙</button>
    <h1>👩‍🏫 Admin Dashboard</h1>
    <p style="text-align:center;">{{ now }}</p>
    <table>
        <tr><th>ID</th><th>Name</th><th>Grade</th><th>Section</th><th>Actions</th></tr>
        {% for s in students %}
        <tr>
            <td>{{ s.id }}</td>
            <td>{{ s.name }}</td>
            <td>{{ s.grade }}</td>
            <td>{{ s.section }}</td>
            <td>
                <a href="{{ url_for('edit_student', id=s.id) }}">Edit</a> |
                <a href="{{ url_for('delete_student', id=s.id) }}">Delete</a>
            </td>
        </tr>
        {% endfor %}
    </table>

    <form method="POST" action="{{ url_for('add_student') }}">
        <h3>Add New Student</h3>
        <input type="text" name="name" placeholder="Name" required>
        <input type="text" name="grade" placeholder="Grade" required>
        <input type="text" name="section" placeholder="Section" required>
        <button type="submit">Add</button>
    </form>

    <h2>🕓 Login History</h2>
    <table>
        <tr><th>Name</th><th>Role</th><th>Time</th></tr>
        {% for log in logs %}
        <tr>
            <td>{{ log.name }}</td>
            <td>{{ log.role }}</td>
            <td>{{ log.time }}</td>
        </tr>
        {% endfor %}
    </table>

    <div style="text-align:center; margin-top:20px;">
        <a href="{{ url_for('logout') }}">Logout</a>
    </div>

    <script>
        function toggleDark() {
            const isDark = document.body.style.getPropertyValue('--bg') === '#111';
            document.body.style.setProperty('--bg', isDark ? '#fff7fa' : '#111');
            document.body.style.setProperty('--text', isDark ? 'black' : 'white');
        }
    </script>
</body>
</html>
"""

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
        }
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

# --------------------------------
# RUN APP
# --------------------------------
if __name__ == '__main__':
    app.run(debug=True)
