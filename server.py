import socket
#from threading import Lock, Thread
from socket import create_server
import threading
from _thread import *
import teamlocaltactics
import DBHandler


class server:
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = []

    def turn_on(self):
        #adr = socket.gethostbyname(socket.gethostname())
        #port = 5550

        self.sock = create_server((self.host, self.port), reuse_port=True)

        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.bind((self.host, self.port))
        #self.sock.listen()

        #self.serving = True

        print("Looking for connection")
        print(socket.gethostbyname(socket.gethostname()))


    def turn_off(self):
        self.sock.close()
        #self.serving = False

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

    #def show_champs():
     #   champions = DBHandler.get_champs()

"""
    while True:
        conn, addr = sock.accept()
        print("Connected to: ", addr)
        start_new_thread(threaded_client, (conn,))
"""

if __name__=="__main__":
    host = socket.gethostbyname(socket.gethostname())
    print(host)
    port = 5550
    server = server(host, port)
    server.turn_on()
    server.turn_off()
    
