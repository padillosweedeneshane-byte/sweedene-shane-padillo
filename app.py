from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey"

students = [
    {"id": 1, "name": "John Doe", "grade": 10, "section": "Zechariah"},
    {"id": 2, "name": "Jane Smith", "grade": 9, "section": "Levi"}
]

login_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Management System</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(-45deg, #ffe6f0, #ffd6e0, #ffe6f0, #ffd6e0);
            background-size: 400% 400%;
            animation: gradient 8s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            transition: background 0.5s, color 0.5s;
        }

        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            width: 400px;
            text-align: center;
            transition: background 0.5s, color 0.5s;
        }

        h2 {
            margin-bottom: 20px;
            background: linear-gradient(90deg, #ff0057, #ff6ec7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 26px;
            animation: colorShift 3s infinite alternate;
        }

        @keyframes colorShift {
            0% { background: linear-gradient(90deg, #ff0057, #ff6ec7); -webkit-background-clip: text; }
            100% { background: linear-gradient(90deg, #ff6ec7, #ff0057); -webkit-background-clip: text; }
        }

        input {
            width: 90%;
            padding: 10px;
            margin: 8px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 14px;
            text-align: center;
        }

        button {
            background: linear-gradient(90deg, #ff0057, #ff6ec7);
            border: none;
            color: white;
            padding: 12px 35px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
            animation: colorShift 3s infinite alternate;
            margin-top: 15px;
        }

        button:hover {
            transform: scale(1.07);
        }

        .dark-mode {
            background: linear-gradient(-45deg, #1a1a1a, #2b2b2b, #1a1a1a, #2b2b2b);
            color: white;
        }

        .dark-mode .container {
            background: #2e2e2e;
            color: white;
        }

        .dark-mode input {
            background: #444;
            color: white;
            border: 1px solid #777;
        }

        .dark-mode button {
            color: white;
        }

        .theme-toggle {
            position: fixed;
            top: 20px;
            right: 30px;
            background: linear-gradient(90deg, #ff0057, #ff6ec7);
            border: none;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            animation: colorShift 3s infinite alternate;
        }
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="toggleTheme()">🌗 Toggle Theme</button>
    <div class="container">
        <h2>Student Management System</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Name (Admin or Student)" required><br>
            <input type="text" name="grade" placeholder="Grade (or 0000 for Admin)" required><br>
            <button type="submit">Login</button>
        </form>
    </div>

    <script>
        function toggleTheme() {
            document.body.classList.toggle("dark-mode");
        }
    </script>
</body>
</html>
"""

student_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Dashboard</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(-45deg, #ffe6f0, #ffd6e0, #ffe6f0, #ffd6e0);
            background-size: 400% 400%;
            animation: gradient 8s ease infinite;
            text-align: center;
            padding: 50px;
        }

        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            display: inline-block;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }

        h2 {
            color: #ff0057;
        }

        .recommendation {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            background: #ffe6f0;
            color: #333;
            font-size: 15px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }

        a {
            display: inline-block;
            margin-top: 20px;
            text-decoration: none;
            background: linear-gradient(90deg, #ff0057, #ff6ec7);
            color: white;
            padding: 10px 25px;
            border-radius: 20px;
            animation: colorShift 3s infinite alternate;
        }

        @keyframes colorShift {
            0% { background: linear-gradient(90deg, #ff0057, #ff6ec7); }
            100% { background: linear-gradient(90deg, #ff6ec7, #ff0057); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, {{ student.name }}!</h2>
        <p>Grade: {{ student.grade }}</p>
        <p>Section: {{ student.section }}</p>
        <div class="recommendation">
            {% if student.grade >= 10 %}
                <b>Recommendation:</b> Great job! Prepare for your senior high transition. Review key topics and explore your future strand choices.
            {% else %}
                <b>Recommendation:</b> Keep up the hard work! Focus on building strong fundamentals in Math and English.
            {% endif %}
        </div>
        <a href="/">Logout</a>
    </div>
</body>
</html>
"""

admin_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(-45deg, #fff0f5, #ffd6e0, #fff0f5, #ffd6e0);
            background-size: 400% 400%;
            animation: gradient 8s ease infinite;
            text-align: center;
            padding: 50px;
        }

        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        table {
            margin: auto;
            border-collapse: collapse;
            width: 70%;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ffb6c1;
        }

        th {
            background: #ff0057;
            color: white;
        }

        h2 {
            color: #ff0057;
        }

        a {
            display: inline-block;
            margin-top: 20px;
            text-decoration: none;
            background: linear-gradient(90deg, #ff0057, #ff6ec7);
            color: white;
            padding: 10px 25px;
            border-radius: 20px;
            animation: colorShift 3s infinite alternate;
        }

        @keyframes colorShift {
            0% { background: linear-gradient(90deg, #ff0057, #ff6ec7); }
            100% { background: linear-gradient(90deg, #ff6ec7, #ff0057); }
        }
    </style>
</head>
<body>
    <h2>Admin Dashboard</h2>
    <table>
        <tr><th>ID</th><th>Name</th><th>Grade</th><th>Section</th></tr>
        {% for s in students %}
        <tr>
            <td>{{ s.id }}</td>
            <td>{{ s.name }}</td>
            <td>{{ s.grade }}</td>
            <td>{{ s.section }}</td>
        </tr>
        {% endfor %}
    </table>
    <a href="/">Logout</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        grade = request.form['grade'].strip()

        if name.lower() == "admin" and grade == "0000":
            session.clear()
            session["admin"] = True
            return redirect(url_for('admin_dashboard'))

        student = next((s for s in students if s["name"].lower() == name.lower() and str(s["grade"]) == grade), None)
        if not student:
            new_id = len(students) + 1
            student = {"id": new_id, "name": name, "grade": int(grade), "section": "Unassigned"}
            students.append(student)

        session.clear()
        session["student"] = student
        return redirect(url_for('student_dashboard'))

    return render_template_string(login_page)

@app.route('/student')
def student_dashboard():
    if "student" not in session:
        return redirect(url_for('login'))
    return render_template_string(student_page, student=session["student"])

@app.route('/admin')
def admin_dashboard():
    if "admin" not in session:
        return redirect(url_for('login'))
    return render_template_string(admin_page, students=students)

if __name__ == '__main__':
    app.run(debug=True)
