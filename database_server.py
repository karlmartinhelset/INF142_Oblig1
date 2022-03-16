from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

from core import Champion

class DBHandler:

  def __init__(self):
    # collection in the database created in get_database() where chamions are stored
    self.Champ_collection = self.get_database()["Champions_collection"]

    # collection in the database created in get_database() where match history is stored
    self.Match_collection = self.get_database()["Match_history_collection"]

    
  def get_database(self):
    # Get the password from .env file
    password = os.getenv("PASSWORD")

    clusterName = "Oblig1142Cluster"

    # Connect to the cluster
    client = MongoClient("mongodb+srv://hannahmorken:" + password + "@Oblig1142Cluster.clrn2.mongodb.net/TeamNetworkTactics", tlsCAFile=certifi.where())

    # Create a new database in the cluster
    database = client["TeamNetworkTactics"]
    return database

  
  def get_champs(self):
    all_champions = {} 

    # loop through each champion in the collection
    for x in self.Champ_collection.find():
        # get champion with name, rockProbability, paperProbability and scissorsProbability
        champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorsProbability"]))
        
        # add champion to new dict
        all_champions[x["Name"]] = champion
        
    return all_champions
  
  
  def add_new_match(self, match):
    self.Match_collection.insert_one(match)

    
def db_main():
  while True:
    DBHandler()

if __name__ == "__main__":
  db_main()

