from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="exam"
)

mycursor = mydb.cursor()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Render the login page when the route is accessed with GET
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        sql = "SELECT * FROM student WHERE username = %s AND password = %s"
        val = (username, password)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()

        if result:
            # Successful login
            return 'Welcome to Exam portal!'
        else:
            return 'Invalid login credentials'
        
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        # Render the signup page when the route is accessed with GET
        return render_template('signup.html')
       
    elif request.method == 'POST':
        # Handle form submission when data is sent using POST
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            # Insert the user into the database
            sql = "INSERT INTO student (username, password) VALUES (%s, %s)"
            val = (username, password)
            mycursor.execute(sql, val)

            mydb.commit()

        #     # Successful signup
        #     return f'Account created for {username}!'
        # else:
        #     return 'Passwords do not match'
        
        @app.route('/login', methods=['GET', 'POST'])
        def signup():
            if request.method == 'GET':
                # Render the signup page when the route is accessed with GET
                return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)
    


