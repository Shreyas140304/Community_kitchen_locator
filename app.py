from flask import Flask,redirect,request,url_for,flash,render_template,session,jsonify
import json
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key="secret-key"
# configuration for mysql database connection is done.
app.config['MYSQL_HOST'] = 'localhost' # 'localhost' means it's running on your own machine.
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ngo_listing'
app.config['MYSQL_DATABASE_DEBUG'] = True

mysql = MySQL(app) # an instance of mysql is created

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # fetch by username and verify hashed password
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account and check_password_hash(account.get('pass',''), password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            flash('Login successful!', 'success')
            return redirect(url_for("welcome"))
        else:
             flash('Invalid credentials. Please try again.', 'error')
    # render on GET or failed POST
    return render_template('LoginForm.html')

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return render_template("base.html")
                    
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
                    username, pass, email, NGO_Name, NGO_Regi,
                    establish_date, contact_Name, phone_num, address,city, state, pincode, 
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (username, hashed_pw, email, ngo_name, ngo_regi,
                    establish_date, contact_name, phone_num, address,city, state, pincode))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            return redirect(url_for('login'))
            
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template("RegisterForm.html", msg=msg)

# The routes required for  authentication (login, logout, register) are defined above.

#---------------------------------------------------------------------------------------------------------------------------------

# Now, we define the welcome route that shows the welcome page after login.

@app.route("/welcome",methods=["POST","GET"]) #- This defines a route /login that accepts 
def welcome(): #both POST and GET HTTP methods. GET is used to show the login form; POST is used to submit login credentials.
     if 'loggedin' in session: # require login to view welcome
         if request.method == "POST":
            fields = ['kitchen_name','address','zip','service_area',
                      'contact_Name','phone_num','contact_email','directions',
                      'days','meal_time','frequency','special_hours',
                      'meal_types','audience','capacity','sts']
            data = {}
            for field in fields:
                 values = request.form.getlist(field)
                 if len(values) > 1:
                      data[field] = json.dumps(values)  # Store as JSON string
                 else:
                      data[field] = values[0] if values else None  # Store single value or None
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
            INSERT INTO kitchens (
                    kitchen_name, address, zip, service_area, contact_Name, phone_num,
                    contact_email, directions, days, meal_time, frequency, special_hours,
                    meal_types, audience, capacity, 
                    sts) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (data['kitchen_name'], data['address'], data['zip'], data['service_area'],
                  data['contact_Name'], data['phone_num'], data['contact_email'], data['directions'],
                  data['days'], data['meal_time'], data['frequency'], data['special_hours'],
                  data['meal_types'], data['audience'], data['capacity'], data['sts'].lower()))
            mysql.connection.commit()
            flash('Kitchen details submitted successfully!', 'success')
            
            return redirect(url_for('display_kitchens'))
         
     return redirect(url_for('display_kitchens'))

@app.route("/display_kitchens")
def display_kitchens():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM kitchens')
        kitchens = cursor.fetchall()
        print("Fetched kitchens are:")
        print(kitchens)

        # For displaying no.of kitchens on the dashboard
        cursor.execute('SELECT COUNT(*) AS total FROM kitchens')
        count = cursor.fetchone()['total']

        # For displaying no. of active kitchens on the dashboard
        cursor.execute('SELECT COUNT(sts) AS active FROM kitchens WHERE sts = "active"')
        count_active = cursor.fetchone()['active']

        flash('Kitchens loaded successfully!', 'success')
        return render_template("NgoWelcome.html",
                                username=session.get('username'), 
                                kitchens=kitchens, 
                                count=count,
                                count_active=count_active)
    return redirect(url_for('login'))

@app.route('/find_food', methods=["GET","POST"])
def find_food():
        if request.method == "POST":
            zip = request.form.get("zip")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM kitchens WHERE zip = %s', (zip,))
            kitchens = cursor.fetchall()
            return render_template("findfood.html", kitchens=kitchens)
        return render_template("findfood.html")

@app.route('/get_kitchen/<int:id>')
def get_kitchen(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM kitchens WHERE id = %s', (id,))
    kitchen = cursor.fetchone()
    return jsonify(kitchen)

@app.route("/edit_kitchen", methods=["POST","GET"])
def edit_kitchen():
     if 'loggedin' in session:
          try:
            if request.method == "POST":
                fields = ['kitchen_name','address','zip','service_area','contact_Name','phone_num','contact_email','directions','days','meal_time','frequency','special_hours','meal_types','audience','capacity','sts']
                data = {}
                for field in fields:
                        values = request.form.getlist(field)
                        if len(values) > 1:
                            data[field] = json.dumps(values)  # Store as JSON string
                        else:
                            data[field] = values[0] if values else None  # Store single value or None

                kitchen_id = request.form.get("id")
                print("Updating kitchen ID:", kitchen_id)

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('''
                    UPDATE kitchens SET
                        kitchen_name=%s, address=%s, zip=%s, service_area=%s, contact_Name=%s, phone_num=%s,
                        contact_email=%s, directions=%s, days=%s, meal_time=%s, frequency=%s, special_hours=%s,
                        meal_types=%s, audience=%s, capacity=%s, sts=%s
                        WHERE id = %s
                    ''' , (data['kitchen_name'], data['address'], data['zip'], data['service_area'], data['contact_Name'], data['phone_num'], data['contact_email'], data['directions'], data['days'], data['meal_time'], data['frequency'], data['special_hours'], data['meal_types'], data['audience'], data['capacity'], data['sts'].lower(), kitchen_id))
                mysql.connection.commit()
                flash('Kitchen details updated successfully!', 'success')
                return '', 200
            
          except Exception as e:
            print("Update error:", e)
            return 'Update failed', 500
          
     return redirect(url_for('login'))

# Now the dashboard part ends.
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# From here the donation and feedback pages routes are created.

@app.route("/feedback",methods=["POST","GET"])
def feedback():
        if request.method == "POST":
            name = request.form.get("username")
            email = request.form.get("email")
            detail = request.form.get("detail")
            rating = request.form.get("rating")
            comments = request.form.get("comments")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''
            INSERT INTO kitchen_feedback (
                    username, email, detail, rating, comments
                ) VALUES (%s, %s, %s, %s, %s)
            ''', (name, email, detail, rating, comments))
            mysql.connection.commit()
            flash('Feedback submitted successfully!', 'success')
            return render_template("base.html")
        return render_template("feedback.html")

@app.route("/donation")
def donation():
    return render_template("donation.html")

