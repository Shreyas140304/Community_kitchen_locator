from flask import Flask,redirect,request,url_for,render_template,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key="secret-key"
credentials = {
    "username":"admin",
    "password":"123"
}
# configuration for mysql database connection is done.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'geekprofile'

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
        cursor.execute(
            'SELECT * FROM accounts WHERE username = %s \ AND password = % s', (username,password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']0
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return redirect(url_for("register"))
        else:
            msg = 'Incorrect username or password !'
        return render_template('login.html',msg=msg)

    #     if (credentials["username"]==username and credentials["password"]==password):
    #         session["user"] = username
    #         print("Login successful")
    #         return redirect(url_for("register"))
    #     else:
    #         print("Login failed")
    #         return redirect(url_for("login"))
    # return render_template("LoginForm.html")

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login')
                    
@app.route("/register",methods=["POST","GET"])
def register():
    if "user" in session:
        if request.method == "POST":
            # we are using 
            ngo_name = request.form.get("NGO_Name")
            ngo_regi = request.form.get("NGO_Regi")
            username = request.form.get("username")
            contact_name = request.form.get("contact_Name")
            phone_num = request.form.get("phone_num")
            email = request.form.get("email")
            address = request.form.get("address")
            city = request.form.get("city")
            state = request.form.get("state")
            pincode = request.form.get("pincode")
            establish_date = request.form.get("establish_date")
            password = request.form.get("password")

            cursor = mysql.connection,cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s',(username,))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
            else:
            cursor.execute('INSERT INTO accounts VALUES \
            (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s)',
                           (username, password, email, 
                            organisation, address, city,
                            state, country, postalcode, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
       elif request.method == 'POST':
            msg = 'Please fill out of the form !'
       return render_template("RegisterForm.html")
                
