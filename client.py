#from copyreg import pickle
import socket
import pickle

from teamlocaltactics import main

class PlayerClient:
    
    def __init__(self, host, port):
        
        self.server = host
        self.port = port
        #self.addr = (self.server, self.port)
    
    def start_client(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server, self.port))
        self.send_recv()
    
    def turn_off(self):
        self.client.close
    
    def send_recv(self):
        while True:
            data = self.client.recv(2048).decode()

            if data:
                data = pickle.loads(data)
                print(data)

            else:
                continue

    # def main_client():
    #     host = socket.gethostbyname(socket.gethostname())
    #     port = 5550
    #     pc = PlayerClient(host, port)
    #     pc.start_client()
    #     pc.turn_off()

if __name__ == "__main__":
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    port = 5550
    pc = PlayerClient(host, port)
    pc.start_client()
    pc.turn_off()