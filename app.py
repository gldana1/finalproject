import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

connection = sqlite3.connect("movies.db")
db = connection.cursor()
db.execute("SELECT * FROM users")

#@app.route("/")
#def homepage():
    #//TODO//

#//List of TODO//

#//Grab API from imdb//

