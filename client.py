#from copyreg import pickle
import socket
import pickle

import teamlocaltactics as tlt
from rich import print

class PlayerClient:
    
    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        #self.addr = (self.server, self.port)
    
    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.get_msg()
    
    def turn_off(self):
        self.client.close
        print("Closed connection to server.")

    
    def get_msg(self):
        while True:
            data = self.client.recv(4098)

            if not data:
                continue

            data = pickle.loads(data)

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
                

            """match data["CMD"]:
                
                case "MSG":
                    print(data["Value"])
                
                case "WELCOME":
                    tlt.print_welcome_msg()
                    
                case "GET_CHAMPS":
                    tlt.print_available_champs(data["Value"])

                case "CHOOSE_CHAMP":
                    args = data["Args"]
                    champ = tlt.input_champion(args["Player"], args["color"], args["champs"], args["team1"], args["team2"])
                    print(champ)
                    self.client.send(champ.encode())
                
                case "PRINT_MATCH":
                    tlt.print_match_summary(data["Value"])"""


                

    # def main_client():
    #     host = socket.gethostbyname(socket.gethostname())
    #     port = 5550
    #     pc = PlayerClient(host, port)
    #     pc.start_client()
    #     pc.turn_off()

if __name__ == "__main__":
    #host = socket.gethostbyname(socket.gethostname())
    host = 'localhost'
    port = 5550
    pc = PlayerClient(host, port)
    pc.start_client()
    pc.turn_off()