import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


connection = sqlite3.connect("movies.db" , check_same_thread=False)
connection.row_factory = dict_factory
db = connection.cursor()

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password", 403)

        # Query database for username
        username = request.form.get("username")
        rows = db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchall()

        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            flash("invalid username and/or password", 403)

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
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        if not request.form.get("username"):
            flash("username cannot be blank")
            return redirect("/login")
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect("/login")
        elif not request.form.get("confirmation") == request.form.get("password"):
            flash("password not confirmed")
            return redirect("/login")
    tmp = request.form.get("password")
    username = request.form.get("username")
    print(username)
    hash = generate_password_hash(request.form.get("password"))
    try:
        db.execute("INSERT INTO users (username, hash) VALUES (?,?)",(username,hash))
        connection.commit()
    except ValueError:
        flash("user already exists")
    return render_template("login.html")

rows = db.execute("SELECT * FROM users").fetchall()

print(rows)
@app.route("/")
def homepage():
    return render_template("index.html")

#//List of TODO//

#//Grab API from imdb//

