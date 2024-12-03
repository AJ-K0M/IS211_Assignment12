import sqlite3

connection = sqlite3.connect('hw13.db')
cursor = connection.cursor()

with open('schema.sql') as f:
    cursor.executescript(f.read())

cursor.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", ("John", "Smith"))
cursor.execute(
    "INSERT INTO quizzes (subject, number_of_questions, date) VALUES (?, ?, ?)",
    ("Python Basics", 5, "2015-02-05")
)
cursor.execute(
    "INSERT INTO results (student_id, quiz_id, score) VALUES (?, ?, ?)",
    (1, 1, 85)
)

connection.commit()
connection.close()
