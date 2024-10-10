from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
import mysql.connector as myconn
import io
from flask_cors import CORS
from send_mail import SEND_MAIL

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)  # Enable CORS for all routes

try:
    conn = myconn.connect(
        host='127.0.0.1',
        user='root',
        password="Kashif@#2001#@", 
        database="user_authentication"
)
    cursor = conn.cursor()
except Exception as e:
    print(f"Error connecting to MySQL: {e}")
    conn,cursor = None, None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/login')
def user_login():
    return render_template('login.html')

@app.route('/apply_for_job')
def apply_for_job():
    return render_template('job_apply.html')


# user registration
@app.route('/register')
def register():
    return render_template('register.html')

# admin registration
@app.route('/admin_register')
def admin_register():
    return render_template('Admin_registration.html')

#admin checking the application
@app.route('/admin_checks_applications')
def admin_check_applications():
    return render_template('admin_checking_applications.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('home')
    
@app.route('/greet')
def greet():
    return render_template('greet.html')   

@app.route("/Applicant_profile_verify")
def send():
    return render_template("Applicant_profile_verify.html")
 
##///////////////////////////////////////////////////////////////////////////////////////////////////
@app.route('/login_validation', methods=['POST','GET'])
def login_validation():
    email=request.form.get('Email')
    password=request.form.get('Password')    
     
    cursor.execute("SELECT * FROM users WHERE Email = %s AND Password = %s",(email,password))
    users= cursor.fetchall()
    print(users)
    if len(users)>0:  # If user credentials are valid
        session['user_id'] = users[0][0]
        return redirect(url_for('apply_for_job'))  # Redirect to the job application page
    else:
        return render_template('error.html') 
    
    
#USER Registration    
@app.route('/registration', methods=['POST','GET'])
def registration():
    Name = request.form.get('uname')  
    Email = request.form.get('uemail')
    Password = request.form.get('upassword')
    
    #password condition
    from Password_handling import Password_
    Password_handle=Password_(Password)
    response = Password_handle.password_handling()
    if response == 1:
        pass
    else:
        return response
    
    cursor.execute("Insert into users (Name,Email,Password) values (%s, %s, %s)",( Name,Email,Password))
    conn.commit()
    
    cursor.execute("SELECT * FROM users WHERE Email = %s",(Email,))
    mydata = cursor.fetchall()
    session['user_id'] = mydata[0][0]
    
    send_mail = SEND_MAIL('Creating account','Your TechSphere account has been successfully created',Email)
    send_mail.send()
    return redirect('login')

## applying for the job
@app.route('/job_application', methods=['POST','GET'])
def job_application():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    phone = request.form.get('pno')
    dob = request.form.get('date')
    role = request.form.get('role')
    
    cursor.execute("Insert into job_application_data (fname,lname,email,phone,dob,jobrole) values (%s,%s,%s,%s,%s,%s)",(fname,lname,email,phone,dob,role))
    conn.commit()
    name = fname+' '+lname
    send_mail = SEND_MAIL('Job Application',f'Dear {name},\nYour job application for the role of {role} has been successfully submitted to TechSphere',email)
    send_mail.send()
    
    return redirect('greet')
#////////////////////////////////////////--ADMIN--/////////////////////////////////////////////////////////////    

#Admin Registration    
@app.route('/admin_registration', methods=['POST','GET'])
def admin_registration():
    Name = request.form.get('aname')  
    Email = request.form.get('aemail')
    Password = request.form.get('apassword')
    
    #password condition
    from Password_handling import Password_
    Password_handle=Password_(Password)
    response = Password_handle.password_handling()
    if response == 1:
        pass
    else:
        return response
    
    cursor.execute("Insert into admin (name,email,password) values (%s, %s, %s)",( Name,Email,Password))
    conn.commit()
    
    return redirect('admin_login')
# admin login
@app.route('/admin_login_validate', methods=['POST','GET'])
def admin_login_validation():
    email=request.form.get('Email')
    password=request.form.get('Password')    
     
    cursor.execute("SELECT * FROM admin WHERE email = %s AND password = %s",(email,password))
    users= cursor.fetchall()
    print(users)
    if len(users)>0:  # If user credentials are valid
        session['user_id'] = users[0][0]
        return redirect('Applicant_profile_verify')  # Redirect to the home page
    else:
        return render_template('error.html') 
    
# logout
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')


#////////////////////////////////////////////////////////////////////////////////////////////////
#Retrieving data of job applications
@app.route('/get_application_data', methods=['GET'])
def get_application_data():
    job_data = cursor.execute("SELECT * FROM job_application_data")
    print(job_data)
    
    
    
''' Inserting The files into the DataBase'''
# getting the data from the client        
'''
@app.route('/job_application', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file= request.files['file'] 
        file.save('K:\PYSPIDERS\PYTHON\ASSIGNMENT_3\static'+file.filename) 
        
        with open('K:\PYSPIDERS\PYTHON\ASSIGNMENT_3\static'+file.filename, 'rb') as file:
            binary_data = file.read()
    

    # Step 3: SQL query to insert the image
    
    cursor.execute("INSERT INTO job_application_data (resume) VALUES (%s)",(binary_data,))  
    conn.commit()
    return 'Your File is uploaded successfully'
    '''


# retrieve the file from mysql for verification


@app.route("/send_data", methods=["GET"])
def send_data():
    try:

        cursor.execute("SELECT * FROM job_application_data")
        job_data = cursor.fetchall()
        response = jsonify(job_data)
        # print(job_data)
        return response
        
    except Exception as e:
        print(f"Error connecting to MySQL: {e}")
        return jsonify({"error": "Failed to retrieve data"}), 500



if __name__ == '__main__':
    app.run(debug=True)