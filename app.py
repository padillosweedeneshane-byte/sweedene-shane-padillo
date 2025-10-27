<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Student Management System</title>
  <style>
    /* ---------- Base Styles ---------- */
    body {
      font-family: 'Poppins', sans-serif;
      background: #f9f9fb;
      color: #333;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      padding-top: 40px;
      margin: 0;
    }

    .container {
      background: #fff;
      padding: 40px 60px;
      border-radius: 20px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      width: 90%;
      max-width: 850px;
      transition: all 0.3s ease;
    }

    h1 {
      text-align: center;
      color: #e91e63;
      margin-bottom: 30px;
      font-size: 28px;
    }

    h2 {
      color: #444;
      font-size: 20px;
      margin-bottom: 10px;
    }

    /* ---------- Form Section ---------- */
    .form-section {
      text-align: center;
      margin-bottom: 25px;
    }

    input {
      padding: 10px;
      margin: 5px;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 14px;
      width: 180px;
    }

    button {
      background: #e91e63;
      color: white;
      border: none;
      padding: 10px 18px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s;
      font-size: 14px;
      margin-top: 5px;
    }

    button:hover {
      background: #c2185b;
    }

    /* ---------- Table ---------- */
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }

    th, td {
      border-bottom: 1px solid #ddd;
      text-align: center;
      padding: 10px;
      font-size: 15px;
    }

    th {
      background: #ffebf1;
      color: #e91e63;
    }

    .delete-btn {
      background: #f44336;
      border: none;
      color: white;
      border-radius: 5px;
      padding: 6px 12px;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    .delete-btn:hover {
      background: #d32f2f;
    }

    hr {
      margin: 20px 0;
      border: 0.5px solid #eee;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🎓 Student Management System</h1>

    <!-- Add Student Form -->
    <div class="form-section">
      <h2>Add Student</h2>
      <input type="text" id="name" placeholder="Name">
      <input type="number" id="grade" placeholder="Grade">
      <input type="text" id="section" placeholder="Section">
      <button onclick="addStudent()">➕ Add Student</button>
    </div>

    <hr>

    <!-- Student List -->
    <div class="list-section">
      <h2>Student List</h2>
      <table id="studentTable">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Grade</th>
            <th>Section</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <!-- Students will appear here -->
        </tbody>
      </table>
    </div>
  </div>

  <script>
    // Load all students
    async function loadStudents() {
      const res = await fetch('/students');
      const data = await res.json();
      const tbody = document.querySelector('#studentTable tbody');
      tbody.innerHTML = '';

      data.forEach(s => {
        const row = `
          <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>${s.grade}</td>
            <td>${s.section}</td>
            <td>
              <button class="delete-btn" onclick="deleteStudent(${s.id})">🗑️ Delete</button>
            </td>
          </tr>`;
        tbody.innerHTML += row;
      });
    }

    // Add new student
    async function addStudent() {
      const name = document.getElementById('name').value.trim();
      const grade = document.getElementById('grade').value.trim();
      const section = document.getElementById('section').value.trim();

      if (!name || !grade || !section) {
        alert("Please fill out all fields!");
        return;
      }

      await fetch('/students', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, grade, section })
      });

      document.getElementById('name').value = '';
      document.getElementById('grade').value = '';
      document.getElementById('section').value = '';
      loadStudents();
    }

    // Delete student
    async function deleteStudent(id) {
      if (!confirm("Are you sure you want to delete this student?")) return;
      await fetch(`/students/${id}`, { method: 'DELETE' });
      loadStudents();
    }

    // Initial load
    loadStudents();
  </script>
</body>
</html>

