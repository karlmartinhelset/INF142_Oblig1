from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import os
import certifi

from core import Champion

# Function to get the database 
class DBHandler:

  def __init__(self, host: str, port: int, buffer_size: int = 2048) -> None:
    self._host = host
    self._port = port
    self._buffer_size = buffer_size
    self._connections = []


  def start(self):
    self._serv_sock = create_server((self._host, self._port))
     while True:
      try:
        conn, _ = self._serv_sock.accept()
      except:
        pass 
      else:
        # Add connection to list
        self._connections.append(conn)
        # Start listening
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


  Champ_collection = get_database()["Champions_collection"]
  Match_collection = get_database()["Match_history_collection"]

  def get_msg(self):
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

  def add_new_champ(self, champion):
    Champ_collection.insert_one(champion)


  def get_champs(self):
    all_champions = {} 
    for x in Champ_collection.find():
        champion = Champion(x["Name"], float(x["rockProbability"]), float(x["paperProbability"]), float(x["scissorsProbability"]))
        all_champions[x["Name"]] = champion
    return all_champions

  # Match history

  def add_new_match(self, match):
    Match_collection.insert_one(match)


  def get_match_history(self, nMatches):
    matchList = Match_collection.find({}).limit(nMatches)
    return matchList

if __name__ == "__main__":
  server = os.environ.get("SERVER", "localhost")
  port = 7020
  serv = DBServer(server, port)
  serv.start()