from flask import Flask, render_template, request, redirect, url_for, jsonify
import os 
import psycopg2
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__, template_folder='templates')
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)


def db_connection():
    conn = psycopg2.connect(url)
    return conn

@app.route("/get-user/<user_id>")
def get_user(user_id):
    user_data = {
        "user_id" : user_id,
        "name" : "Cameron Poe",
        "email" : "cameron.poe@iocleaning.com"

    }
    extra = request.args.get("extra")
    if extra:
        user_data["extra"]=extra
    return jsonify(user_data),200

   
@app.route('/')
def index():
    return render_template('index.html')  # Landing page

# Route to handle both GET and POST for adding an employee
@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':  # Handle form submission
        # Get data from form fields
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        hire_date = request.form['hire_date']
        job_title = request.form['job_title']
        salary = float(request.form['salary'])
        department = request.form['department']

        # Connect to the database and insert data
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, salary, department)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, hire_date, job_title, salary, department))

        # Commit and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('index'))  # Redirect back to the landing page after success

    # Handle GET request (just show the form)
    return render_template('add-employee.html')  # Show the form when GET is called

if __name__ == '__main__':
    app.run(debug=True)

