from flask import Flask,redirect,request,url_for,render_template,session

app = Flask(__name__)

app.secret_key="secret-key"
credentials = {
    "username":"admin",
    "password":"123"
}
@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if (credentials["username"]==username and credentials["password"]==password):
            session["user"] = username
            print("Login successful")
            return redirect(url_for("register"))
        else:
            print("Login failed")
            return redirect(url_for("login"))
    return render_template("LoginForm.html")


@app.route("/register",methods=["POST","GET"])
def register():
    if "user" in session:
        if request.method == "POST":
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
            return render_template("RegisterForm.html")
        elif request.method == "POST":
                # Handle registration logic here
                return "<h2>Registration successful!</h2>"
    return redirect(url_for("login"))