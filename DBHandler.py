import pymongo
from pymongo import MongoClient
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



# Champions

def add_new_champ(champion):
  Champ_collection.insert_one(champion)


def get_champs():
    all_champions = {} 
    for x in Champ_collection.find():
        champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorProbability"]))
        all_champions[x["Name"]] = champion
    return all_champions



# Match history

def add_new_match(match):
    Match_collection.insert_one(match)


#def get_match_history():