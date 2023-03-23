import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



connection = sqlite3.connect("movies.db")
db = connection.cursor()
rows = db.execute("SELECT * FROM users").fetchall()

print(rows)
#@app.route("/")
#def homepage():
    #//TODO//

#//List of TODO//

#//Grab API from imdb//

