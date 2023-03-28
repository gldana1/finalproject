import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['TEMPLATES_AUTO_RELOAD'] = True
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

apiinput = {"d":
[{"i":{"height":1922,"imageUrl":"https://m.media-amazon.com/images/M/MV5BMDNkOTE4NDQtMTNmYi00MWE0LWE4ZTktYTc0NzhhNWIzNzJiXkEyXkFqcGdeQXVyMzQ2MDI5NjU@._V1_.jpg","width":1280},"id":"tt0386676","l":"The Office","q":"TV series","qid":"tvSeries","rank":86,"s":"Steve Carell, Jenna Fischer","y":2005,"yr":"2005-2013"}
,
{"i":{"height":1377,"imageUrl":"https://m.media-amazon.com/images/M/MV5BOTA5MzQ3MzI1NV5BMl5BanBnXkFtZTgwNTcxNTYxMTE@._V1_.jpg","width":930},"id":"tt0151804","l":"Office Space","q":"feature","qid":"movie","rank":1213,"s":"Ron Livingston, Jennifer Aniston","y":1999}
,
{"i":{"height":828,"imageUrl":"https://m.media-amazon.com/images/M/MV5BYWI2YmI2ZmMtMTZjMC00MzMzLWI5ODItNDY1OTg3YjNmZmUxXkEyXkFqcGdeQXVyNDA5NTgxNjU@._V1_.jpg","width":591},"id":"tt0290978","l":"The Office","q":"TV series","qid":"tvSeries","rank":2377,"s":"Ricky Gervais, Martin Freeman","y":2001,"yr":"2001-2003"}
,
{"i":{"height":1350,"imageUrl":"https://m.media-amazon.com/images/M/MV5BNmFjZDE2YzQtOWZhOC00MzA4LWEyMDYtNWEyMDE2MGFjZThkXkEyXkFqcGdeQXVyMTI1OTkzMzQ5._V1_.jpg","width":1080},"id":"tt20877972","l":"The Office","q":"TV series","qid":"tvSeries","rank":11282,"s":"Saleh Abuamrh, Fahad Albutairi","y":2022,"yr":"2022-2023"}
,
{"i":{"height":1276,"imageUrl":"https://m.media-amazon.com/images/M/MV5BYzgyZjE1MjUtYjFjZS00NzMzLWFmNWMtMDJjNGY0ZTgwYjc3XkEyXkFqcGdeQXVyMjQwMjk0NjI@._V1_.jpg","width":882},"id":"tt1711525","l":"Office Christmas Party","q":"feature","qid":"movie","rank":9925,"s":"Jason Bateman, Olivia Munn","y":2016}
,
{"i":{"height":1440,"imageUrl":"https://m.media-amazon.com/images/M/MV5BODJlNDcxNzMtODBlYS00Yzc1LTg2NDEtNDJkYTlkNmM0NWY2XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg","width":1000},"id":"tt6251024","l":"Office Uprising","q":"feature","qid":"movie","rank":16595,"s":"Brenton Thwaites, Jane Levy","y":2018}
,
{"i":{"height":1702,"imageUrl":"https://m.media-amazon.com/images/M/MV5BMjk2MzU0ZGItZjkwNi00YTZjLThkMmMtZWE1N2U0NGY0NjY5XkEyXkFqcGdeQXVyMjk1MjQ3NzI@._V1_.jpg","width":1156},"id":"tt12194000","l":"Out of Office","q":"TV movie","qid":"tvMovie","rank":10310,"s":"Ken Jeong, Jay Pharoah","y":2022}
,
{"i":{"height":400,"imageUrl":"https://m.media-amazon.com/images/M/MV5BYTc3MDkzZDEtZjI4OC00YzAwLWI4YjUtZDllZTFhYWNhYTJjXkEyXkFqcGdeQXVyNjExODE1MDc@._V1_.jpg","width":286},"id":"tt0292829","l":"Office Office","q":"TV series","qid":"tvSeries","rank":44931,"s":"Pankaj Kapur, Deven Bhojani","y":2000}]
,"q":"office","v":1}


#print(rows)
@app.route("/search")
def search():
    return render_template("search.html", apiinput=apiinput)
    
@app.route("/search/<id>", methods=["GET", "POST"])
def searchid(id):
    data = id
    return render_template("test.html", apiinput=apiinput, data=data)


#//List of TODO//

#//Grab API from imdb//

