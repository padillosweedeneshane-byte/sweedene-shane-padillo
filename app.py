from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# Start with an empty student list
students = []

# --------------------------------
# LOGIN PAGE - Anyone can log in
# --------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        grade = request.form['grade'].strip()

        # Admin login
        if name.lower() == "admin" and grade == "0000":
            session.clear()
            session["admin"] = True
            return redirect(url_for('admin_dashboard'))

        # Check if student already exists
        student = next((s for s in students if s["name"].lower() == name.lower()), None)

        # If not found, register automatically
        if not student:
            new_id = len(students) + 1
            student = {"id": new_id, "name": name, "grade": grade, "section": "Unassigned"}
            students.append(student)

        # Log in as student
        session.clear()
        session["student"] = student
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
    return render_template_string(student_dashboard_page, student=student)


# --------------------------------
# ADMIN DASHBOARD
# --------------------------------
@app.route('/admin')
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for('login'))
    return render_template_string(admin_page, students=students)


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
        return redirect(url_for('admin_dashboard'))

    return render_template_string(edit_page, student=student)


# Delete student
@app.route('/admin/delete/<int:id>')
def delete_student(id):
    if "admin" not in session:
        return redirect(url_for('login'))
    global students
    students = [s for s in students if s["id"] != id]
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
            background: #fff7fa;
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
            background: #fdf2f7;
            text-align: center;
            padding: 50px;
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
    </style>
</head>
<body>
    <h1>🎓 Welcome, {{ student.name }}!</h1>
    <div class="card">
        <p><strong>ID:</strong> {{ student.id }}</p>
        <p><strong>Name:</strong> {{ student.name }}</p>
        <p><strong>Grade:</strong> {{ student.grade }}</p>
        <p><strong>Section:</strong> {{ student.section }}</p>
        <a href="{{ url_for('logout') }}"><button>Logout</button></a>
    </div>
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
            background: #fff7fa;
            padding: 30px;
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
        a:hover, button:hover { background: #c2185b; }
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
    </style>
</head>
<body>
    <h1>👩‍🏫 Admin Dashboard</h1>
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
    <div style="text-align:center; margin-top:20px;">
        <a href="{{ url_for('logout') }}">Logout</a>
    </div>
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
