from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        flash('Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    connection = sqlite3.connect('hw13.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    students = cursor.execute("SELECT * FROM students").fetchall()
    quizzes = cursor.execute("SELECT * FROM quizzes").fetchall()
    connection.close()
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        connection = sqlite3.connect('hw13.db')
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
            connection.commit()
            flash('Student added successfully.')
            return redirect(url_for('dashboard'))
        except:
            flash('Error adding student.')
        finally:
            connection.close()
    return render_template('add_student.html')

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        subject = request.form['subject']
        number_of_questions = request.form['number_of_questions']
        date = request.form['date']
        connection = sqlite3.connect('hw13.db')
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO quizzes (subject, number_of_questions, date) VALUES (?, ?, ?)", 
                           (subject, number_of_questions, date))
            connection.commit()
            flash('Quiz added successfully.')
            return redirect(url_for('dashboard'))
        except:
            flash('Error adding quiz.')
        finally:
            connection.close()
    return render_template('add_quiz.html')

@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    connection = sqlite3.connect('hw13.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        quiz_id = request.form.get('quiz_id')
        score = request.form.get('score')
        try:
            cursor.execute("INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)", 
                           (student_id, quiz_id, score))
            connection.commit()
            flash("Quiz result added successfully.")
            return redirect(url_for('dashboard'))
        except:
            flash("Error adding quiz result.")
        finally:
            connection.close()
    students = cursor.execute("SELECT id, first_name, last_name FROM students").fetchall()
    quizzes = cursor.execute("SELECT id, subject FROM quizzes").fetchall()
    connection.close()
    return render_template('add_results.html', students=students, quizzes=quizzes)

@app.route('/student/<int:student_id>')
def view_results(student_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    connection = sqlite3.connect('hw13.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    student = cursor.execute("SELECT first_name, last_name FROM students WHERE id = ?", (student_id,)).fetchone()
    results = cursor.execute("""
        SELECT quizzes.id AS quiz_id, quizzes.subject AS quiz_subject, results.score
        FROM results
        JOIN quizzes ON results.quiz_id = quizzes.id
        WHERE results.student_id = ?
    """, (student_id,)).fetchall()
    connection.close()
    return render_template('view_results.html', student=student, results=results)

if __name__ == '__main__':
    app.run(debug=True)
