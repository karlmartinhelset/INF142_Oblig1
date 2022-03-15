import socket
#from threading import Lock, Thread
from socket import create_server
from unittest.main import main
from xmlrpc.client import Server

import teamlocaltactics 
import DBHandler
from DBHandler import *

import pickle

from rich import print

from core import Match, Team
from core import *


class server:
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = []
        self.team1 = []
        self.team2 = []

    def turn_on(self):
        #self.sock = create_server((self.host, self.port), reuse_port=True)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        

        print("hei")
        
        self.DB_sock = socket.create_connection((self.host, 7020))
        
        self.sock.listen()
        print("Looking for connection")
        #self.serving = True
        self.accept_conn()


    def turn_off(self):
        self.sock.close()
        print("Server is closed")

    def accept_conn(self):
        while True:
            try:
                conn, _ = self.sock.accept()
            except:
                pass
            else:
                self.connections.append(conn)

                if(len(self.connections) == 1):
                    data = {
                        "CMD": "MSG",
                        "Value": "Waiting for other player"
                    }
                    #msg = "Not enough players! Waiting to start game ..."
                    self.connections[0].send(pickle.dumps(data))
                
                else:
                    self.run_game()

        #     match len(self.connections):
        #         case 1:
        #             #self.connections[0].send("Not enough players! Waiting to start game ...".encode())
        #             msg = "Not enough players! Waiting to start game ..."
        #             self.connections[0].send(pickle.dumps(msg))
        #         case 2:
        #             print("Enough players connected! Starting the game...")
        #             break

        # self.run_game()



    def send_everyone(self, message):
        for connection in self.connections:
            connection.send(pickle.dumps(message))
            

    def get_team(self, nr):
        if nr == 1:
            choosingIndex = 0
            #sendIndex = 1
            color = "red"

        else:
            choosingIndex = 1
            #sendIndex = 0
            color = "blue"

        data = {
            "CMD": "CHOOSE_CHAMP",
            "Args": {
                "Player": "Player " + str(nr),
                "color": color,
                "champs": self._champions,
                "team1": self.team1,
                "team2": self.team2,
            }
        }
        
        self.connections[choosingIndex].send(pickle.dumps(data))

        while True:
            champ = self.connections[choosingIndex].recv(1024).decode()

            if not champ:
                continue
            
            if nr == 1:
                self.team1.append(champ)
            else:
                self.team2.append(champ)
            break


    def run_game(self):
        data = {
            "CMD": "WELCOME"
        }
        # send message to each client
        self.send_everyone(data)

        DBdata = {
            "CMD": "GETALLCHAMPS"
        }

        # Ask the database connection to recieve all champions
        self.DB_sock.send(pickle.dumps(DBdata))
        self._champions = pickle.loads(self.DB_sock.recv(2048))

        # fetch champions from database
        #self.champions = DBHandler.get_champs()
        # create a table containing the champions
        data = {
            "CMD": "GET_CHAMPS",
            "Value": self._champions
        }
        # send table to each client
        self.send_everyone(data)

        # get players
        # ask client for player teams
        # get the teams from client
        for _ in range(2):
            self.get_team(1)
            self.get_team(2)

        # create match from the match class with the two teams
        match = Match(
                Team([self._champions[name] for name in self.team1]),
                Team([self._champions[name] for name in self.team2])
            )
        # play match. Use match.play()
        match.play()

        # get match result from team_local_tactics.print_match_summary(match)
        data = {
            "CMD": "PRINT_MATCH",
            "Value": match
        }
        # send result to client
        self.send_everyone(data)

        #upload match result to database
        DBdata = {
            "CMD": "UPLOADMATCH",
            "Value": match.to_dict()
        }
        
        #DBHandler.add_new_match(match)
        #self.send_everyone(match)
        
        self.DB_sock.send(pickle.dumps(DBdata))

    # def main_server(self):
    #     host = socket.gethostbyname(socket.gethostname())
    #     port = 5550
    #     server = server(host, port)
    #     server.turn_on()
    #     server.turn_off()


if __name__ == "__main__":
    #host = socket.gethostbyname(socket.gethostname())
    host = 'localhost'
    port = 5550
    servr = server(host, port)
    servr.turn_on()
    servr.turn_off()
    
