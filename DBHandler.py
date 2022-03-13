import pymongo
from pymongo import MongoClient
from flask import Flask, render_template
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

from core import Champion

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


Champ_collection = get_database()["Champions_collection"]
Match_collection = get_database()["Match_history_collection"]

def get_msg():
  while True:
    for conn in self._connections:
      # Try to recv data
      data = conn.recv(self._buffer_size)

      # Continue if no data
      if not data:
        continue

      # Load data with pickle
      data = pickle.loads(data)

      # Match commands
      match data["CMD"]:
        case "ADDCHAMP":
          add_new_champ(data["Value"])
        case "GETALLCHAMPS":
          champs = get_champs()
          conn.send(pickle.dumps(champs))
        case "UPLOADMATCH":
          add_new_match(data["Value"])
        case "GETMATCHES":
          matches = getMatchHistory(data["Value"])
          conn.send(pickle.dumps(matches))

# Champions

def add_new_champ(champion):
  Champ_collection.insert_one(champion)


def get_champs():
  all_champions = {} 
  for x in Champ_collection.find():
      champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorsProbability"]))
      all_champions[x["Name"]] = champion
  return all_champions

# Match history

def add_new_match(match):
  Match_collection.insert_one(match)


def get_match_history(nMatches):
  matchList = Match_collection.find({}).limit(nMatches)
  return matchList



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