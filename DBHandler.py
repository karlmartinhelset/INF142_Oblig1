import pymongo
from pymongo import MongoClient
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