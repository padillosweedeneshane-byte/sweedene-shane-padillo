from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# Sample student list (acts like a database)
students = [
    {"id": 1, "name": "John Doe", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Jane Smith", "grade": 11, "section": "Reuben"}
]

# --------------------------------
# LOGIN PAGE
# --------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip().lower()
        grade = request.form['grade']

        for s in students:
            if s["name"].lower() == name and str(s["grade"]) == grade:
                session["student"] = s
                return redirect(url_for('dashboard'))
        return render_template_string(login_page, error="Account not found. Please sign up below.")

    return render_template_string(login_page)

# --------------------------------
# SIGNUP PAGE
# --------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        grade = request.form['grade']
        section = request.form['section'].strip()

        # Check if already exists
        for s in students:
            if s["name"].lower() == name.lower() and str(s["grade"]) == grade:
                return render_template_string(signup_page, error="This student already exists!")

        # Add new student
        new_id = len(students) + 1
        new_student = {"id": new_id, "name": name, "grade": int(grade), "section": section}
        students.append(new_student)
        session["student"] = new_student
        return redirect(url_for('dashboard'))

    return render_template_string(signup_page)

# --------------------------------
# DASHBOARD
# --------------------------------
@app.route('/dashboard')
def dashboard():
    if "student" not in session:
        return redirect(url_for('login'))
    student = session["student"]
    return render_template_string(dashboard_page, student=student)

# --------------------------------
# LOGOUT
# --------------------------------
@app.route('/logout')
def logout():
    session.pop("student", None)
    return redirect(url_for('login'))

# --------------------------------
# HTML Templates (Inline)
# --------------------------------

login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Login</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: #fff7fa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-box {
            background: #fff;
            padding: 40px 50px;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            width: 350px;
            text-align: center;
        }
        h1 {
            color: #e91e63;
        }
        input {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
        }
        button:hover {
            background: #c2185b;
        }
        .error {
            color: red;
        }
        a {
            color: #e91e63;
            text-decoration: none;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>Student Login</h1>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="POST">
            <input type="text" name="name" placeholder="Full Name" required><br>
            <input type="number" name="grade" placeholder="Grade Level (e.g. 10)" required><br>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="{{ url_for('signup') }}">Sign Up</a></p>
    </div>
</body>
</html>
"""

signup_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Sign Up</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: #fdf2f7;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .signup-box {
            background: #fff;
            padding: 40px 50px;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            width: 350px;
            text-align: center;
        }
        h1 {
            color: #e91e63;
        }
        input {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
        }
        button:hover {
            background: #c2185b;
        }
        .error {
            color: red;
        }
        a {
            color: #e91e63;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="signup-box">
        <h1>Sign Up</h1>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="POST">
            <input type="text" name="name" placeholder="Full Name" required><br>
            <input type="number" name="grade" placeholder="Grade Level" required><br>
            <input type="text" name="section" placeholder="Section" required><br>
            <button type="submit">Create Account</button>
        </form>
        <p>Already have an account? <a href="{{ url_for('login') }}">Login</a></p>
    </div>
</body>
</html>
"""

dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
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
        h1 {
            color: #e91e63;
        }
        p {
            font-size: 16px;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
        }
        button:hover {
            background: #c2185b;
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

if __name__ == '__main__':
    app.run(debug=True)
            
