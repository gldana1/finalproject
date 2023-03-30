import os
import requests
import os
import sqlite3
import requests
from flask import Flask, flash, redirect, render_template, request, session
from flask_session.__init__ import Session
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
import json

from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

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
            try:
                stars = row["s"]
            except:
                stars = ""
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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d