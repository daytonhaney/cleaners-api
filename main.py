from flask import Flask, render_template, request, redirect, url_for, jsonify
import os 
import psycopg2
from dotenv import load_dotenv
from db.database import customers_table

load_dotenv()
url = os.getenv("DATABASE_URL")
app = Flask(__name__, template_folder='templates')
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)

cx_table = customers_table()

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
    """Landing page
    """
    return render_template('index.html')

@app.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        hire_date = request.form['hire_date']
        job_title = request.form['job_title']
        salary = float(request.form['salary'])
        department = request.form['department']

        conn = psycopg2.connect(url)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, salary, department)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """, 
                       (first_name, last_name, email, phone, hire_date, job_title, salary, department))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    return render_template('add-employee.html')

@app.route('/view-employees')
def view_employee():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from employees")
    employees = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("view-employees.html",employees=employees)

@app.route('/view-customers',methods=['GET'])
def view_customers():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("select * from customers")
    customers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("view-customers.html",customers=customers)

@app.route('/new-jobs',methods=['GET'])
def new_jobs():
    return render_template("new-jobs.html")


@app.route('/completed-jobs',methods=['GET'])
def completed_jobs():
    return render_template("completed-jobs.html")

@app.route('/equipment',methods=['GET'])
def equipment():
    return render_template("equipment.html")





if __name__ == '__main__':
    app.run(debug=True)

