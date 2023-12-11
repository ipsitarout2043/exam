from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="exam"
)

mycursor = mydb.cursor()

# Endpoint to display exam questions
@app.route('/exam')
def exam():
    mycursor.execute("SELECT * FROM questions")
    questions = mycursor.fetchall()
    return render_template('exam.html', questions=questions)

# Endpoint to process exam submission
@app.route('/submit_exam', methods=['POST'])
def submit_exam():
    score = 0
    total_questions = 0

    mycursor.execute("SELECT * FROM questions")
    questions = mycursor.fetchall()

    for question in questions:
        user_answer = request.form.get(f"question_{question[0]}")
        if user_answer and user_answer == question[2]:  # Assuming correct_answer is in the third column
            score += 1
        total_questions += 1

    percentage = (score / total_questions) * 100

    return render_template('result.html', score=score, total_questions=total_questions, percentage=percentage)

if __name__ == '__main__':
    app.run(debug=True)
