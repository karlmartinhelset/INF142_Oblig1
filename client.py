#from copyreg import pickle
import socket
import pickle

import teamlocaltactics as tlt

class PlayerClient:
        
    def __init__(self):
        host = 'localhost'
        port = 5550
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

        self.get_msg()
    
    def turn_off(self):
        self.client.close
        print("Closed connection to server.")
    
    def get_msg(self):
        while True:
            data = self.client.recv(4098)
            #print(not data)

            if not data:
                continue

            data = pickle.loads(data)
            #print(data)

            match data["CMD"]:
                
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
                    tlt.print_match_summary(data["Value"])
                

if __name__ == "__main__":
    
    playerclient = PlayerClient()