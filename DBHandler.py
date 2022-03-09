import pymongo
from pymongo import MongoClient
from flask import Flask, render_template
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

# Function to get the database 
def get_database():

  # Get you password from .env file
  password = os.getenv("PASSWORD")

  username = "hannahmorken"
  clusterName = "Oblig1142Cluster"

  # Connect to you cluster
  client = MongoClient("mongodb+srv://hannahmorken:" + password + "@Oblig1142Cluster.clrn2.mongodb.net/TeamNetworkTactics", tlsCAFile=certifi.where())

  # Create a new database in your cluster
  database = client["TeamNetworkTactics"]
  return database


def get_collection(collection):
  db = get_database()
  return db[collection]



# Champions

def add_new_champ(champion):
  collection = get_collection("Champions_collection")
  collection.insert_one(champion)


#def get_champs():



# Match history

def add_new_match(match):
    collection = get_collection("Match_history_collection")
    collection.insert_one(match)


#def get_match_history():

#Flask
#This is so that we can see the information from MongoDB on a webpage
app = Flask(__name__)
#app.config["MONGO_URI"] = "mongodb+srv://hannahmorken:5550"
#mongo = PyMongo(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/Match_History/')
def Match_History():
  return render_template('Match_History.html')

@app.route('/Champions/')
def Champions():
  return render_template('Champions.html')

if __name__=='__main__':
      app.run()