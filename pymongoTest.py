from shelve import DbfilenameShelf
import pymongo
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask.json import jsonify
from dotenv import load_dotenv
load_dotenv()
import os
import DBHandler

app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb+srv://hannahmorken:<password>@oblig1142cluster.clrn2.mongodb.net/test"
#app.config["MONGO_URI"] = DBHandler.get_database()
#mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Match_History/')
def Match_History():
    return render_template('Match_History.html')

@app.route('/Champions/')
def Champions():
    champs = DBHandler.Champ_collection.data.find({"Name": "Ola"})
    #champions = DBHandler.get_champs()
    print(DBHandler.Champ_collection.data.find({}))
    #return render_template('Champions.html', champs = champs)
    return jsonify([DBHandler.Champ_collection.data.find({})])
    #return jsonify([DBHandler.Champ_collection.data.find({})])

if __name__=='__main__':
    app.run()