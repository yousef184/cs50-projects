import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

 apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

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





@app.route("/")
@login_required
def index():
    db.execute("DELETE FROM shares WHERE shares = ?",0)
    rows = db.execute("SELECT * FROM shares WHERE id = ?", session["user_id"])
    rows1 = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    return render_template("index.html",rows =rows,cash =float(rows1[0]["cash"]), lookup=lookup )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        if not request.form.get("shares").isdigit() or int(request.form.get("shares")) < 1:
            return apology("share must be at least 1", 400)
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        quote = lookup(symbol)
        if not symbol:
            return apology(message ="no symbol entered" )
        if not quote:
            return apology(message ="no symbol found")
        if shares <= 0:
            return apology(message ="shares should be positive" )
        price = float(quote["price"]*shares/1.00)
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if rows[0]["cash"] < price:
            return apology(message ="Can't afford")
        db.execute("UPDATE users SET cash = ? WHERE id = ?", rows[0]["cash"]*1.00 - (price* shares/1.00),session["user_id"] )
        if db.execute("SELECT symbol FROM shares WHERE id = ? AND symbol = ?", session["user_id"],symbol):
            db.execute("UPDATE shares SET shares = shares + ? WHERE symbol = ? AND id = ?",shares,symbol,session["user_id"])
        else:
            db.execute("INSERT INTO shares (id,symbol,shares) VALUES(?,?,?)",session["user_id"], symbol.upper(),shares)
        date = datetime.now()
        time = date.strftime("%d/%m/%y") + " " + date.strftime("%H:%M:%S")
        db.execute("INSERT INTO history (id,symbol,shares,time) VALUES(?,?,?,?)",session["user_id"], symbol,shares,time)
        return redirect("/")
    else:
        return render_template("buy.html")
@app.route("/history")
@login_required
def history():
    rows = db.execute("SELECT * FROM history WHERE id = ?", session["user_id"])
    return render_template("history.html", rows = rows, lookup = lookup)


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


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        if not request.form.get("symbol") :
            return apology(message ="no symbol entered")
        if lookup(request.form.get("symbol")) == None:
            return apology(message ="no symbol found")
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        name = quote["name"]
        price = quote["price"]
        return render_template("quoted.html",name = name ,price = price ,symbol = symbol )
    else:
        return render_template("quote.html")


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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
      if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))
        quote = lookup(symbol)
        rows = db.execute("SELECT * FROM shares WHERE symbol = ? AND id = ?", symbol,session["user_id"])
        if not shares or shares < 0:
            return apology(message ="please enter valid number of shares" )
        if not symbol:
            return apology(message ="no symbol entered" )
        if not quote:
            return apology(message ="no symbol found")
        if rows[0]["shares"] - shares < 0:
            return apology(message ="not enough shares" )
        price = quote["price"]*(-shares)
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", rows[0]["cash"] + price ,session["user_id"] )
        date = datetime.now()
        time = date.strftime("%d/%m/%y") + " " + date.strftime("%H:%M:%S")
        db.execute("INSERT INTO history (id,symbol,shares,time) VALUES(?,?,?,?)",session["user_id"], symbol.upper(),-shares,time)
        db.execute("UPDATE shares SET shares = shares + ? WHERE symbol = ? AND id = ?",(-shares),symbol,session["user_id"])
        return redirect("/")
      else:
        rows = db.execute("SELECT * FROM shares WHERE id = ?", session["user_id"])
        return render_template("sell.html", rows = rows)

@app.route("/addCash", methods=["GET", "POST"])
@login_required
def addCash():
    if request.method == "POST":
        if not (request.form.get("cash")) :
             return apology(message ="enter valid cash number")
        cash = int(request.form.get("cash"))
        if cash <=0:
             return apology(message ="enter valid cash number")
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        db.execute("UPDATE users SET cash = ? WHERE id = ?", rows[0]["cash"] + cash ,session["user_id"] )
        return redirect("/")
    else:
        return render_template("addCash.html")