from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secretkey"

students = [
    {"id": 1, "name": "John Doe", "grade": 10, "section": "Levi"},
    {"id": 2, "name": "Jane Smith", "grade": 12, "section": "Zechariah"}
]

def assign_section(grade):
    """Automatically assign a section based on grade level."""
    grade = int(grade)
    if 7 <= grade <= 8:
        return "Genesis"
    elif 9 <= grade <= 10:
        return "Levi"
    elif 11 <= grade <= 12:
        return "Zechariah"
    else:
        return "Faith"

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
            background: linear-gradient(-45deg, #ffd1dc, #ffe6f0, #ffd6e0, #ffcce0);
            background-size: 400% 400%;
            animation: gradient 10s ease infinite;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            transition: background 0.5s, color 0.5s;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            width: 420px;
            text-align: center;
        }
        h2 {
            margin-bottom: 15px;
            background: linear-gradient(90deg, #ff0057, #ff6ec7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 28px;
            animation: colorShift 3s infinite alternate;
        }
        @keyframes colorShift {
            0% { background: linear-gradient(90deg, #ff0057, #ff6ec7); -webkit-background-clip: text; }
            100% { background: linear-gradient(90deg, #ff6ec7, #ff0057); -webkit-background-clip: text; }
        }
        input {
            width: 90%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 12px;
            border: 1px solid #ccc;
            font-size: 15px;
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
            font-size: 16px;
            margin-top: 10px;
            transition: transform 0.3s, box-shadow 0.3s;
            animation: glow 2s infinite alternate;
        }
        @keyframes glow {
            from { box-shadow: 0 0 10px #ff6ec7; }
            to { box-shadow: 0 0 25px #ff0057; }
        }
        button:hover { transform: scale(1.05); }
        .recommendation-box {
            background: linear-gradient(90deg, #fff0f5, #ffe6f0);
            border-radius: 15px;
            padding: 15px;
            margin-top: 25px;
            font-size: 14px;
            color: #333;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            animation: fadein 1.2s ease;
        }
        @keyframes fadein {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Student Management System</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Name (Admin or Student)" required><br>
            <input type="text" name="grade" placeholder="Grade (or 0000 for Admin)" required><br>
            <button type="submit">Login</button>
        </form>
        <div class="recommendation-box" id="recommendationBox">💡 Loading recommendations...</div>
    </div>
    <script>
        const tips = [
            "📘 Tip: Always double-check your grade before logging in.",
            "🌟 Admin uses 'Admin' and '0000' to access the dashboard.",
            "🎓 Stay motivated! Every login is a step closer to success.",
            "📅 Keep your section updated for better organization.",
            "💖 Switch to dark mode for a more relaxed view.",
            "⚡ Fun fact: You can add unlimited students!"
        ];
        function showTip() {
            const box = document.getElementById('recommendationBox');
            const tip = tips[Math.floor(Math.random() * tips.length)];
            box.innerHTML = tip;
        }
        setInterval(showTip, 4000);
        showTip();
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
            background: #ffe6f0;
            text-align: center;
            padding: 50px;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            display: inline-block;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        }
        h2 { color: #ff0057; }
        p { color: #555; }
        a { color: #ff0057; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome, {{ student.name }}!</h2>
        <p>Grade: {{ student.grade }}</p>
        <p>Section: {{ student.section }}</p>
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
            background: #fff0f5;
            text-align: center;
            padding: 50px;
        }
        table {
            margin: auto;
            border-collapse: collapse;
            width: 70%;
            background: white;
        }
        th, td {
            padding: 10px;
            border: 1px solid #ffb6c1;
        }
        th {
            background: #ff0057;
            color: white;
        }
        h2 { color: #ff0057; }
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
    <br>
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

        # Auto-assign section when new student logs in
        student = next((s for s in students if s["name"].lower() == name.lower() and str(s["grade"]) == grade), None)
        if not student:
            new_id = len(students) + 1
            section = assign_section(grade)
            student = {"id": new_id, "name": name, "grade": int(grade), "section": section}
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
