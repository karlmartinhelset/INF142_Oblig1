import socket

class PlayerClient:
    
    def __init__(self):
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5550
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print(self.p)
    
    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect((self.server, self.port))
            return self.client.recv(2048).decode()
        except:
            pass
    
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


pc = PlayerClient()
print(pc.send("hello"))
print(pc.send("working"))
