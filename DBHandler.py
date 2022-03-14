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

  def __init__(self, host: str, port: int, buffer_size: int = 2048) -> None:
    self._host = host
    self._port = port
    self._buffer_size = buffer_size
    self._connections = []
    self.Champ_collection = self.get_database()["Champions_collection"]
    self.Match_collection = self.get_database()["Match_history_collection"]


  def start(self):
    self._serv_sock = create_server((self._host, self._port))
    #self._serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self._serv_sock.bind((self._host, self._port))
    while True:
      try:
        conn, _ = self._serv_sock.accept()
      except:
        pass 
      else:
        
        self._connections.append(conn)
        
        self.get_msg()


  def get_database(self):

    # Get you password from .env file
    password = os.getenv("PASSWORD")

    username = "hannahmorken"
    clusterName = "Oblig1142Cluster"

    # Connect to you cluster
    client = MongoClient("mongodb+srv://hannahmorken:" + password + "@Oblig1142Cluster.clrn2.mongodb.net/TeamNetworkTactics", tlsCAFile=certifi.where())

    # Create a new database in your cluster
    database = client["TeamNetworkTactics"]
    return database


  # Champ_collection = get_database()["Champions_collection"]
  # Match_collection = get_database()["Match_history_collection"]

  def get_msg(self):
    while True:
      for conn in self._connections:
        
        data = conn.recv(self._buffer_size)

        if not data:
          continue

        data = pickle.loads(data)

        match data["CMD"]:
          case "ADDCHAMP":
            self.add_new_champ(data["Value"])
          case "GETALLCHAMPS":
            champs = self.get_champs()
            conn.send(pickle.dumps(champs))
          case "UPLOADMATCH":
            self.add_new_match(data["Value"])
          case "GETMATCHES":
            matches = self.get_match_history(data["Value"])
            conn.send(pickle.dumps(matches))


  def add_new_champ(self, champion):
    self.Champ_collection.insert_one(champion)


  def get_champs(self):
    all_champions = {} 
    for x in self.Champ_collection.find():
        champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorsProbability"]))
        all_champions[x["Name"]] = champion
    return all_champions


  # Match history

  def add_new_match(self, match):
    self.Match_collection.insert_one(match)


  def get_match_history(self, nMatches):
    matchList = self.Match_collection.find({}).limit(nMatches)
    return matchList


if __name__ == "__main__":
  server = os.environ.get("SERVER", "localhost")
  port = 7020
  serv = DBHandler(server, port)
  serv.start()

