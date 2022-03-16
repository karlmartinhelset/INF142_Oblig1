
import socket
import pickle

import teamlocaltactics as tlt
from rich import print

class PlayerClient:
        
    def __init__(self):
        host = 'localhost'
        port = 5550

        # create and connect socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.get_data()
    
    def turn_off(self):
        self.client.close
        print("Closed connection to server.")

    
    def get_data(self):
        while True:
            # recieve data from socket
            data = self.client.recv(4098)

            if not data:
                continue

            data = pickle.loads(data)

            # different actions based on the messages the client has recieved
            if data[0] == "Waiting":
                print(data[1])

            elif data[0] == "Welcome":
                print(data[1])

            elif data[0] == "Choose player":
                chosen = tlt.input_champion(data[1], data[2], data[3], data[4], data[5])
                print(chosen)
                self.client.send(chosen.encode())
                
            elif data[0] == "Get champs":
                tlt.print_available_champs(data[1])
                
            elif data[0] == "Print match":
                tlt.print_match_summary(data[1])
         

if __name__ == "__main__":
    playerclient = PlayerClient()