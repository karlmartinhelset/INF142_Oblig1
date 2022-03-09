
import socket
#from threading import Lock, Thread
import threading
from _thread import *
import teamlocaltactics

adr = socket.gethostbyname(socket.gethostname())
port = 5550

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind((adr, port))
   
except socket.error as e:
    str(e)

sock.listen()
print("Looking for connection")
print(socket.gethostbyname(socket.gethostname()))

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

while True:
    conn, addr = sock.accept()
    print("Connected to: ", addr)
    start_new_thread(threaded_client, (conn,))
