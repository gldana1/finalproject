import os
import sqlite3
import csv
import json



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

connection = sqlite3.connect("movies.db" , check_same_thread=False)
connection.row_factory = dict_factory
db = connection.cursor()


dict = []
with open("test2.txt") as file:
    dictfirst = file.read()
    #print(dict)
dictmid = json.loads(dictfirst)
dict = dictmid["d"]
#print (dictfinal)
for row in range(len(dict)):
        
    #print (dict[row].keys())
    url = dict[row]["i"]["imageUrl"]
    ibdb_id = dict[row]["id"]
    title =dict[row]["l"]
    type = dict[row]["q"]
    rank = dict[row]["rank"]
    stars = dict[row]["s"]
    year = dict[row]["y"]
    if "yr" in dict[row]:
        running = dict[row]["yr"]
    db.execute("INSERT INTO movies (url, ibdb_id,title,type,rank,stars,year,running) VALUES (?,?,?,?,?,?,?,?)",(url, ibdb_id,title,type,rank,stars,year,running))
    connection.commit()
    




