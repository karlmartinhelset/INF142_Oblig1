import socket
#from threading import Lock, Thread
from socket import create_server
import threading
from _thread import *

import teamlocaltactics 
import DBHandler

import pickle

from rich import print
from rich.prompt import Prompt
from rich.table import Table


class server:
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = []

    def turn_on(self):
        self.sock = create_server((host, port), reuse_port=True)

        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.bind((self.host, self.port))
        #self.sock.listen()

        self.serving = True
        self.accept_conn()

        print("Looking for connection")


    def turn_off(self):
        self.sock.close()
        self.serving = False

    """
    def threaded_client(conn):
        conn.send(str.encode("Connected"))
        reply = ""
        while True:
            try:
                data = conn.recv(2048)
                reply = data.decode("utf-8")
                print(reply)
                print(data)

                if not data:
                    print("Disconnected")
                    break
                else:
                    print("Received: ", reply)
                    print("Sending: ", reply)

                conn.sendall(str.encode(reply))
            
            except:
                break
        
        print('Lost connection')
        conn.close()
    """

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


    def run_game(self):
        welcome_message = '\n'
        'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
        '\n'
        'Each player choose a champion each time.'
        '\n'
        self.send_everyone(welcome_message)

        champions = DBHandler.get_champs()
        table = teamlocaltactics.print_available_champs(champions)
        self.send_everyone(table)




    """
    while True: 
        
        print("Connected to: ", addr)
        start_new_thread(threaded_client, (conn,))
    """

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    port = 5550
    server = server(host, port)
    server.turn_on()
    server.turn_off()
    
