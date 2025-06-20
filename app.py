#from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for

import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Step 7: New route for Add Student page
@app.route('/add', methods=['GET', 'POST'])
@app.route('/add', methods=['GET', 'POST'])
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']

        # Save to DB
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, roll, email) VALUES (?, ?, ?)", (name, roll, email))
        conn.commit()
        conn.close()

        # ✅ Redirect to /students instead of showing plain message
        return redirect(url_for('view_students'))

    return render_template('add.html')

@app.route('/students')
def view_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('students.html', students=students)
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()

    if request.method == 'POST':
        # Update logic
        name = request.form['name']
        roll = request.form['roll']
        email = request.form['email']

        c.execute("UPDATE students SET name = ?, roll = ?, email = ? WHERE id = ?", (name, roll, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_students'))

    # Show edit form with existing data
    c.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = c.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()           # <- call this before starting app
    app.run(debug=True)

