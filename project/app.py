import os
from cs50 import SQL
from PIL import Image
from flask import Flask, flash, redirect, render_template, request, session,url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import login_required, imageToBLOB
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/workspaces/99906529/project/static/profilePics'
ALLOWED_EXTENSIONS = {'png', 'jpg'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///lawyers.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

cities = ["Cairo","Giza","Alexandri","North coast","Qalyubia","Gharbia","Menofia","Fayoum"]
specialities = ["Family Law","Health Law","Criminal Law","Constitutional Law","Property Law"]
images=[]

@app.route("/", methods=["GET", "POST"])
def index():
     if request.method == "POST":
        return redirect("/search")
     else:
        return render_template("index.html",cities = cities,specialities = specialities)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology(message ="must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology(message ="must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology(message ="invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/lawyerRegister",methods=["GET", "POST"])
def lawyerRegister():
    if request.method == "POST":
        file = request.files['file']
        if not request.form.get("username"):
            return apology(message ="must provide username" )

        elif len(db.execute("SELECT * FROM lawyers WHERE username = ?", request.form.get("username"))) != 0:
            return apology(message ="username already exist")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology(message ="must provide password" )

        elif not request.form.get("confirmation"):
            return apology(message ="must provide password confirmation" )

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology(message ="password and password confirmation are not the same" )

        if not request.form.get("city"):
            return apology(message ="must provide city" )

        if not request.form.get("speciality"):
            return apology(message ="must provide speciality" )

        if not request.form.get("gender"):
            return apology(message ="must provide gender" )

        if not request.form.get("fee"):
            return apology(message ="must provide fee" )

        if len(request.form.get("description")) <= 0:
            return apology(message ="must provide username" )

        db.execute("INSERT INTO lawyers (username,hash,description,city,speciality,gender,fees) VALUES(?,?,?,?,?,?,?)",request.form.get("username"),generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8), request.form.get("description"), request.form.get("city"),request.form.get("speciality"),request.form.get("gender"),request.form.get("fee"))

        rows = db.execute("SELECT * FROM lawyers WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology(message ="invalid username and/or password" )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext = str(session["user_id"]) +"."+ filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], ext))
        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("lawyerRegister.html",cities = cities,specialities = specialities)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology(message ="must provide username" )

        elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) != 0:
            return apology(message ="username already exist")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology(message ="must provide password" )

        elif not request.form.get("confirmation"):
            return apology(message ="must provide password confirmation" )

        elif request.form.get("confirmation") != request.form.get("password"):
            return apology(message ="password and password confirmation are not the same" )

        db.execute("INSERT INTO users (username,hash) VALUES(?,?)",request.form.get("username"),generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology(message ="invalid username and/or password" )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/search", methods=["GET", "POST"])
def search():
    
    return render_template("search.html")

