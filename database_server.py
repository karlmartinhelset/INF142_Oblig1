from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

from core import Champion

class DBHandler:

  def __init__(self):
    self.Champ_collection = self.get_database()["Champions_collection"]
    self.Match_collection = self.get_database()["Match_history_collection"]

  def get_database(self):

    # Get you password from .env file
    password = os.getenv("PASSWORD")

    clusterName = "Oblig1142Cluster"

    # Connect to you cluster
    client = MongoClient("mongodb+srv://hannahmorken:" + password + "@Oblig1142Cluster.clrn2.mongodb.net/TeamNetworkTactics", tlsCAFile=certifi.where())

    # Create a new database in your cluster
    database = client["TeamNetworkTactics"]
    return database

  def get_champs(self):
    all_champions = {} 
    for x in self.Champ_collection.find():
        champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorsProbability"]))
        all_champions[x["Name"]] = champion
    return all_champions

  def add_new_match(self, match):
    self.Match_collection.insert_one(match)

def db_main():
  while True:
    DBHandler()

if __name__ == "__main__":
  db_main()