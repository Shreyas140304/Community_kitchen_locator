from flask import Flask,redirect,request,url_for,render_template,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key="secret-key"
credentials = {
    "username":"admin",
    "password":"123"
}

# configuration for mysql database connection is done.
app.config['MYSQL_HOST'] = 'localhost' # 'localhost' means it's running on your own machine.
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql@2025'
app.config['MYSQL_DB'] = 'ngo_listing'
app.config['MYSQL_DATABASE_DEBUG'] = True

mysql = MySQL(app) # an instance of mysql is created

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login",methods=["POST","GET"])
def login():
    msg = ''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # fetch by username and verify hashed password
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account and check_password_hash(account.get('password',''), password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for("welcome"))
        else:
            msg = 'Incorrect username or password !'
    # render on GET or failed POST
    return render_template('LoginForm.html', msg=msg)

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))
                    
@app.route("/register",methods=["POST","GET"])
def register():
    msg = ''
    # require login (login sets 'loggedin')
    if (request.method == "POST"
        and 'NGO_Name' in request.form  and 'NGO_Regi' in request.form 
        and 'establish_date' in request.form and 'contact_Name' in request.form 
        and 'phone_num' in request.form and 'email' in request.form 
        and 'address' in request.form and 'city' in request.form 
        and 'state' in request.form and 'pincode' in request.form 
        and 'username' in request.form and 'password' in request.form):
        ngo_name = request.form.get("NGO_Name")
        ngo_regi = request.form.get("NGO_Regi")
        establish_date = request.form.get("establish_date")
        contact_name = request.form.get("contact_Name")
        phone_num = request.form.get("phone_num")
        email = request.form.get("email")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        pincode = request.form.get("pincode")
        username = request.form.get("username")
        password = request.form.get("password")

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s',(username,)) 
        account = cursor.fetchone()
        if account:
                msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
        else:
            # store hashed password
            hashed_pw = generate_password_hash(password)
            cursor.execute('''
            INSERT INTO accounts (
                    username, password, email, NGO_Name, NGO_Regi,
                    address, contact_Name, phone_num, city,
                    state, pincode, establish_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (username, hashed_pw, email, ngo_name, ngo_regi,
                    address, contact_name, phone_num, city,
                    state, pincode, establish_date))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("RegisterForm.html", msg=msg)

@app.route("/welcome",methods=["POST","GET"]) #- This defines a route /login that accepts 
def welcome(): #both POST and GET HTTP methods. GET is used to show the login form; POST is used to submit login credentials.
     if 'loggedin' in session: # require login to view welcome
         if request.method == "POST":
            # fields = ['kitchen_name','address','pincode','service_area','contact_person','contact_phone','contact_email','accessibility','days','opening_time','closing_time','frequency','meal_types','target_audience','capacity']
            # data = {field: request.form.get(field) for field in fields}
            return render_template("NgoWelcome.html", username=session.get('username'))
     return render_template('NgoWelcome.html')
