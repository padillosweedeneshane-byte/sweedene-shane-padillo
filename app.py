from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"  # Needed for session management

# Sample student accounts (you can add more)
students = [
    {"id": 1, "name": "John Doe", "grade": 10, "section": "Zechariah", "username": "john", "password": "1234"},
    {"id": 2, "name": "Jane Smith", "grade": 11, "section": "Reuben", "username": "jane", "password": "abcd"}
]

# --------------------------------
# LOGIN PAGE
# --------------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for s in students:
            if s["username"] == username and s["password"] == password:
                session["student"] = s
                return redirect(url_for('dashboard'))
        return render_template_string(login_page, error="Invalid username or password")

    return render_template_string(login_page)

# --------------------------------
# DASHBOARD PAGE
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
<html lang="en">
<head>
    <meta charset="UTF-8">
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
            margin-bottom: 20px;
        }
        input {
            width: 90%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
            font-size: 14px;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background: #c2185b;
        }
        .error {
            color: red;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>Student Login</h1>
        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required><br>
            <input type="password" name="password" placeholder="Password" required><br>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

dashboard_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: #fdf2f7;
            color: #333;
            margin: 0;
            padding: 40px;
        }
        h1 {
            color: #e91e63;
            text-align: center;
        }
        .card {
            background: #fff;
            padding: 25px 40px;
            border-radius: 20px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            width: 400px;
            margin: 50px auto;
            text-align: center;
        }
        .info {
            font-size: 16px;
            line-height: 1.8em;
        }
        button {
            background: #e91e63;
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 15px;
            transition: 0.3s;
        }
        button:hover {
            background: #c2185b;
        }
    </style>
</head>
<body>
    <h1>🎓 Welcome, {{ student.name }}!</h1>
    <div class="card">
        <div class="info">
            <p><strong>Student ID:</strong> {{ student.id }}</p>
            <p><strong>Name:</strong> {{ student.name }}</p>
            <p><strong>Grade:</strong> {{ student.grade }}</p>
            <p><strong>Section:</strong> {{ student.section }}</p>
        </div>
        <a href="{{ url_for('logout') }}"><button>Logout</button></a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
