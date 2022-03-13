import socket
#from threading import Lock, Thread
from socket import create_server
from unittest.main import main

import teamlocaltactics 
import DBHandler

import pickle

from rich import print
from rich.prompt import Prompt
from rich.table import Table

from core import Match


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
        self.sock.listen()

        print("Looking for connection")
        self.serving = True
        self.accept_conn()


    def turn_off(self):
        self.sock.close()
        self.serving = False
        print("Server is closed")

    def accept_conn(self):
        while self.serving:
            try:
                conn, _ = self.sock.accept()
            except:
                pass
            self.connections.append(conn)

            match len(self.connections):
                case 1:
                    self.connections[0].send("Not enough players! Waiting to start game ...".encode())
                case 2:
                    print("Enough players connected! Starting the game...")
                    break

        self.run_game()


    def send_everyone(self, message):
        for connection in self.connections:
            connection.send(pickle.dumps(message))

    def get_team(self, nr):
        if nr == 1:
            choosingIndex = 0
            sendIndex = 1
            color = "red"

        else:
            choosingIndex = 1
            sendIndex = 0
            color = "blue"

        data = {
                "MSG": "CHOOSE_CHAMP",
                "player": "Player " + str(nr),
                "color": color,
                "champs": self.champions,
                "team1": self.team1,
                "team2": self.team2
            }
        
        self.connections[choosingIndex].send(pickle.dumps(data))

        while self.serving:
            champ = self.connections[choosingIndex].recv(4098)

            if not champ:
                continue
            champ = pickle.loads(champ)
            if nr == 1:
                self.team1.append(champ)
            else:
                self.team2.append(champ)
            break


    def run_game(self):
        data = {
            "MSG": "WELCOME"
        }
        # send message to each client
        self.send_everyone(data)

        # fetch champions from database
        self.champions = DBHandler.get_champs()
        # create a table containing the champions
        data = {
            "MSG": "GET_CHAMPS",
            "champs": self.champions
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
                Team([self.champions[name] for name in self.player1]),
                Team([self.champions[name] for name in self.player2])
            )
        # play match. Use match.play()
        match.play()

        # get match result from team_local_tactics.print_match_summary(match)
        data = {
            "MSG": "PRINT_MATCH",
            "Value": match
        }
        # send result to client
        self.send_everyone(data)

        # upload match result to database
        DBHandler.add_new_match(match)

    # def main_server(self):
    #     host = socket.gethostbyname(socket.gethostname())
    #     port = 5550
    #     server = server(host, port)
    #     server.turn_on()
    #     server.turn_off()


if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 5550
    server = server("10.111.37.88", port)
    server.turn_on()
    server.turn_off()
    
