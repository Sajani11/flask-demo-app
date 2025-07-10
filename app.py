from flask import Flask, render_template, request, redirect, url_for, session,make_response,flash
import os
from flask_mysqldb import MySQL
import MySQLdb
from werkzeug.security import check_password_hash, generate_password_hash



app = Flask(__name__)
app.secret_key = "ocem@123wp"

mysql = MySQL(app)

UPLOAD_FOLDER="uploads"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
ALLOWED_EXTENSION={'jpg','png','jpeg'}
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
def allowed_file(filenmae):
    pass

users = {}

@app.route('/signup', methods=["GET", "POST"])
def signup():
    error = ""
    form_data = {"name": "", "email": "", "password": "", "repass": ""}
    
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        repass = request.form['repass']

        form_data = {
            "name": name,
            "email": email,
            "password": "", 
            "repass": ""
        }

        if password != repass:
            error = "Passwords do not match"
        elif email in users:
            error = "User already exists"
        else:
            users[email] = {"name": name, "password": password}
            return redirect(url_for("login"))
    
    return render_template("signup.html", error=error, form_data=form_data)


@app.route('/login', methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if not user or user['password'] != password:
            error = "Invalid email or password"
        else:
            session['user'] = user['name']
            return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)


@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if not user:
        return redirect(url_for("login"))
    return f"Welcome, {user}! <a href='/logout'>Logout</a>"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for("login"))
   

# @app.route("/")
# def index():
#      data={"name":"Sajani","age":19}
#      return render_template("index.html",d=data)


@app.route("/")
def index():
     data="sajani"     
     age=19
     return render_template("index.html",d=data,a=age)


# @app.route("/")    #root direct0ry
# def sayhello():
#     return "Hello World "

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/filecss")
def filecss():
    return render_template("index2.html")

@app.route("/about/<data>")
def sayHi(data):
    return f"Hello {data}"

@app.route('/register', methods=["GET", "POST"])
def register():
    error = ""
    form_data = {"name": "", "email": "", "password": "", "repass": ""}

    if request.method == "POST":
        name = request.form['txtfullname']
        email = request.form['txtEmail']
        password = request.form['txtPassword']
        repass = request.form['RetypePassword']
        form_data = {
            "name": name,
            "email": email,
            "password": password,
            "repass": repass
        }

        if password != repass:
            error = "Passwords do not match"
            return render_template("register.html", error=error, form_data=form_data)

        return f"Name: {name} and Email: {email}"

    return render_template("register.html", error=error, form_data=form_data)


@app.route('/admission', methods=["GET", "POST"])
def admission():
    error = ""
    form_data = {
        "name": "",
        "address": "",
        "gender": "",
        "class": "",
        "phone_number": "",
        "admission_date": "",
        "parent_contact_number": "",
        "age": ""
    }

    if request.method == "POST":
        name = request.form.get('txtfullname', '').strip()
        address = request.form.get('txtAddress', '').strip()
        gender = request.form.get('gender', '').strip()
        class_ = request.form.get('Class', '').strip()
        phone_number = request.form.get('phone_num', '').strip()
        admission_date = request.form.get('Admissiondate', '').strip()
        parent_contact_number = request.form.get('parent_num', '').strip()
        age = request.form.get('Age', '').strip()

        form_data = {
            "name": name,
            "address": address,
            "gender": gender,
            "class": class_,
            "phone_number": phone_number,
            "admission_date": admission_date,
            "parent_contact_number": parent_contact_number,
            "age": age
        }

        if not name:
            error = "Name should not be empty"
            return render_template("admission.html", error=error, form_data=form_data)

        session['student_data'] = form_data
        return redirect(url_for('student_details'))

    return render_template("admission.html", error=error, form_data=form_data)

@app.route('/studentdetails')
def student_details():
    student = session.get('student_data')
    if not student:
        return redirect(url_for('admission'))
    return render_template("studentdetails.html", student=student)

@app.route('/products')
def products():
    if "user" in session:
      products=[
        {'name':'Marker','price':120,'image':'image/marker.jpeg','short_description':"Temporary marker with black ink"},
        {'name':'Umbrella','price':420,'image':'image/umbrella.jpeg','short_description':"Protects from rain and sun"},
        {'name':'Bag','price':1200,'image':'image/bag.jpeg','short_description':"Carry your load in comfort "},
        {'name':'Washing machine','price':12000,'image':'image/washing machine.jpeg','short_description':"Fast washing and less electricity consuming"},
        {'name':'LCD','price':120000,'image':'image/lcd.jpeg','short_description':"Thin , light weight with maximun width"}
        ]
      return render_template('products.html',products=products)
    else:
        return redirect(url_for("login"))


@app.route('/visits')
def visitcount():
    if "visit" in session:
        session['visit']=session.get('visit')+1

    else :
        session['visit']=1
    return render_template("visit.html")

@app.route('/deletesession')
def delete():
    session.pop('visit')
    return redirect('/visits')



@app.route('/setcookie')
def cookie():
    resp=make_response("Cookie is set.")
    resp.set_cookie("username" , "Sajani", max_age=60)
    return resp

@app.route('/getcookie')
def Getcookie():
    name=request.cookies.get('username')
    return f"Name :{name}"

@app.route('/deletecookie')
def deletecookie():
    resp=make_response("Cookie delete.")
    resp.set_cookie("username","",expires="0")
    return resp
# write the code to check if the user is new or not then set the 
# cookie username if the user us new . if user is old then welcome them with the username

@app.route('/user/<username>')
def checkuser(username):
    checkuser=request.cookies.get('username')
    if checkuser:
     return f"Hello , Welcome {checkuser}"
    else:
        resp=make_response("Welcome to our System ")
        resp.set_cookie('username',username)
        return resp
    

@app.route('/fileupload')
def fileupload():
    return render_template("upload.html")

@app.route('/upload', methods=["POST"])
def upload_file():
    # pass
    file =request.files['imageupload']  #name of file used i.e imageupload
    if file not in request.files['imageupload']:
        flash ("File not selected")
        return render_template("upload.html")
    # file.save(os.p.ath.join('uploads',file.filename))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
    return "File Uploaded"

   
@app.route('/choose-auth', methods=['GET', 'POST'])
def choose_auth():
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email')
        password = request.form.get('password')

        if action == 'login':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                flash('Login successful!', 'success')

                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('home'))

            flash('Invalid login credentials.', 'danger')

        elif action == 'register':
            name = request.form.get('name')
            hashed_pw = generate_password_hash(password)
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (name, email, hashed_pw))
            mysql.connection.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('choose_auth'))

    return render_template('choose_auth.html')



if __name__ =="__main__":
    app.run(debug=True)


#     venv/Scripts/activate → works in CMD

# venv\Scripts\Activate.ps1 → for PowerShell

# source venv/bin/activate → for Linux/macOS

# source venv/Scripts/activate → correct for Git Bash on Windows
