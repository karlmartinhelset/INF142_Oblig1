import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

# Function to get the database 
def get_database():

  # Get you password from .env file
  password = os.getenv("password")

  username = "hannahmorken"
  clusterName = "Oblig1142Cluster"

  # Connect to you cluster
  client = MongoClient('mongodb+srv://' + username + ':' + password + '@Oblig1142Cluster.clrn2.mongodb.net/INF142', tlsCAFile=certifi.where())

  # Create a new database in your cluster
  database = client["Team Network Tactics"]
  return database


def get_collection(collection):
  db = get_database()
  collection_name = db[collection]



# Champions

def add_new_champ(champion):
  get_collection("Champions_collection")
  collection_name.insert_one(champion)


def get_champions():



# Match history

def get_match_history():