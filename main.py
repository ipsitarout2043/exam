from flask import Flask, render_template, session, request, redirect, url_for
import mysql.connector


app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="examdbase"
)

app.secret_key = 'your_secret_key'

mycursor = mydb.cursor()

@app.route('/')
def home():
    return render_template('Registration.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('Registration.html')
    elif request.method == 'POST':
        Username = request.form['Username']
        Email = request.form['Email']
        Password = request.form['Password']

        sql = "INSERT INTO students (Username, Email, Password) VALUES (%s, %s, %s)"
        val = (Username, Email, Password)
        mycursor.execute(sql, val)
        mydb.commit()
        session['username'] = Username
        return "Signup successful! Username: {}, Email: {}".format(Username, Email)

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['Username']
        email = request.form['Email']
        password = request.form['Password']

        sql = "SELECT * FROM students WHERE Username = %s AND Email = %s AND Password = %s"
        val = (username, email, password)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        if result:
            session['username'] = username
            return redirect(url_for('exam'))
        else:
            return "Login failed. Invalid username, email, or password."

@app.route('/exam')
def exam():
    return render_template('exam.html')


@app.route('/getUser', methods=['POST'])
def get_user():
    data = []

    if request.method == "POST":

        try:
            mycursor.execute('SELECT * FROM quens')
            result = mycursor.fetchall()

            for row in result:
                data.append({
                    "qid": row[0],  # Assuming the first column is the question_id
                    "question": row[1],
                    "A": row[2],
                    "B": row[3],
                    "C": row[4],
                    # Add the correct column index for selected_option
                    "selected_option": row[5]  # Update with the correct column index
                })

            return render_template('exam.html', data=data)

        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred."
    
    return render_template('exam.html', data=data)  # Provide a default value for username

@app.route('/exam_submit', methods=['GET', 'POST'])
def exam_submit():
    data = []

    if request.method == "POST":
        # username = request.form.get("username")
        username = session.get('username')
        try:
            mycursor.execute('SELECT * FROM quens')
            result = mycursor.fetchall()
            user_responses = [] 
            for row in result:
                question_id = row[0]
                ans_key = "ans" + str(question_id)
                selected_option = request.form.get(ans_key)
                user_responses.append((username, question_id, selected_option))

            sql = "INSERT INTO users (username, question_id, selected_option) VALUES (%s, %s, %s)"
            mycursor.executemany(sql, user_responses)
            mydb.commit()
            

            return render_template('result.html', data=data, username=username)

        except Exception as e:
            # Handle exceptions, log, or return an error message
            print(f"Error: {e}")
            return "An error occurred."

    # Handle GET request (initial page load)
    # return render_template('exam.html', data=data)
    return redirect(url_for('result'))


@app.route('/result')
def result():
    username = session.get('username')
    
    query = '''
    SELECT users.username, users.question_id, users.selected_option,
           quens.question AS question_text, quens.correct_ans, quens.correct_option
    FROM users
    INNER JOIN quens ON users.question_id = quens.qid
    WHERE users.username = %s
'''

    mycursor.execute(query, (username,))
    result = mycursor.fetchall()
    
    total_score = 0
    secured_score = 0

    for row in result:
        total_score += 1 
        if row[2] == row[5]:  
            secured_score += 1 
    if total_score > 0:
        result_percentage = (secured_score / total_score) * 10
    else:
        result_percentage = 0

    return render_template('result.html', result=result, username=username, total_score=total_score, secured_score=secured_score, result_percentage=result_percentage)
if __name__ == '__main__':
    app.run(debug=True)
