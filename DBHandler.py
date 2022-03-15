from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import certifi
import socket
from socket import create_server
import pickle

from core import Champion

# Function to get the database 
class DBHandler:

  def __init__(self, host: str, port: int):
    self._host = host
    self._port = port
    self._connections = []
    self.Champ_collection = self.get_database()["Champions_collection"]
    self.Match_collection = self.get_database()["Match_history_collection"]


  def start(self):
    self._serv_sock = create_server((self._host, self._port))
    
    while True:
      conn, _ = self._serv_sock.accept()
      self._connections.append(conn)
      #self.upload_match


  def get_database(self):

    # Get you password from .env file
    password = os.getenv("PASSWORD")

    clusterName = "Oblig1142Cluster"

    # Connect to you cluster
    client = MongoClient("mongodb+srv://hannahmorken:" + password + "@Oblig1142Cluster.clrn2.mongodb.net/TeamNetworkTactics", tlsCAFile=certifi.where())

    # Create a new database in your cluster
    database = client["TeamNetworkTactics"]
    return database


  def add_new_champ(self, champion):
    self.Champ_collection.insert_one(champion)


  def get_champs(self):
    all_champions = {} 
    for x in self.Champ_collection.find():
        champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorsProbability"]))
        all_champions[x["Name"]] = champion
    return all_champions


  # Matches

  def add_new_match(self, match):
    self.Match_collection.insert_one(match)


  def get_match_history(self, nMatches):
    matchList = self.Match_collection.find({}).limit(nMatches)
    return matchList

def db_main():
  host = 'localhost'
  port = 7020
  serv = DBHandler(host, port)
  serv.start()


if __name__ == "__main__":
  db_main()
  # host = 'localhost'
  # port = 7020
  # serv = DBHandler(host, port)
  # serv.start()

