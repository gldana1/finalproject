import os
import sqlite3
import requests
from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
import json

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#api call
def apicall(item):
    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q":item}

    headers = {
        "X-RapidAPI-Key": "de32aed7c6mshc427496794b63e2p151e0fjsn9afca0074b65",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #print(response.text)
    return response.text

#parse and load response
def parse(reply):
    connection = sqlite3.connect("movies.db" , check_same_thread=False)
    connection.row_factory = dict_factory
    db = connection.cursor()
    dictmid = json.loads(reply)
    dict = dictmid["d"]
    print (dict)
    for row in dict:
        for key in row:    
        #print (dict[row].keys())
            try:
                url = row["i"]["imageUrl"]
            except:
                url = ""    
            ibdb_id = row["id"]
            title = row["l"]
            try:
                type = row["q"]
            except:
                type = ""
            try:
                rank = row["rank"]
            except:
                rank = ""
            stars = row["s"]
            try:
                year = row["y"]
            except:
                year = 0    
        #if "yr" in dict[row]:
        #    running = dict[row]["yr"]
            try:
                db.execute("INSERT INTO movies (url, ibdb_id,title,type,rank,stars,year) VALUES (?,?,?,?,?,?,?)",(url, ibdb_id,title,type,rank,stars,year))
                connection.commit()
            except:
                continue
    return



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['TEMPLATES_AUTO_RELOAD'] = True
Session(app)



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
        if not request.form.get("name"):
            name = "user"
        else:
            name = request.form.get("name")
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
    
    #print(username)
    hash = generate_password_hash(request.form.get("password"))
    try:
        db.execute("INSERT INTO users (username, hash, name) VALUES (?,?,?)",(username,hash,name))
        connection.commit()
    except ValueError:
        flash("user already exists")
    return render_template("login.html")

rows = db.execute("SELECT * FROM users").fetchall()

#print(rows)
@app.route("/")
def homepage():
    return render_template("index.html")



#print(rows)
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html")
    if request.method == "POST":
        s = request.form.get("searchbox")
        try:
            parse(apicall(s))
            apiinput = db.execute("SELECT * FROM movies WHERE title LIKE (?)", ['%' + s + '%']).fetchall()
        except:
            flash("Please enter in searchbox")
            return render_template("search.html")
        return render_template("searched.html", apiinput=apiinput)
    
@app.route("/search/<id>", methods=["GET", "POST"])
def searchid(id):
    if request.method == "GET":
        data = id
        info = db.execute("SELECT * FROM movies WHERE ibdb_id LIKE (?)", [data]).fetchall()
        #print(info)
        return render_template("test.html", info=info, data=data)
    if request.method == "POST":
        if  request.form["addfav"]:
            wl = request.form.get("addfav")
            data = id
            user = session["user_id"]
            movie_id= db.execute("SELECT id FROM movies WHERE ibdb_id LIKE id").fetchone()
            db.execute("INSERT INTO favorites (user_id,movie_id,watchlist) VALUES (?,?,1)", (user,movie_id))
            connection.commit()
            return redirect("/mylist")
        if  request.form["addwat"]:
            wl = request.form.get("addwat")
            data = id
            user = session["user_id"]
            movie_id= db.execute("SELECT id FROM movies WHERE ibdb_id LIKE id").fetchone()
            db.execute("INSERT INTO favorites (user_id,movie_id,watched) VALUES (?,?,1)", (user,movie_id))
            connection.commit()
            return redirect("/mylist")
       
@app.route("/mylist/")
def mylist():
    user = session["user_id"]
    return render_template("mylist.html")



#//List of TODO//

#//Grab API from imdb//

