import socket
print(socket.gethostbyname(socket.gethostname()))
class PlayerClient:
    
    def __init__(self, host, port):
        
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5550
        self.addr = (self.server, self.port)
        self.p = self.connect()
        print(self.p)
    
    def turn_on(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.server, self.port))
        
    
    def send(self):
        while True:
            data = self.client.recv(2048).decode()

            if data:
                self.client.send(str.encode(data))

            else:
                continue


    # def connect(self):
    #     try:
    #         self.client.connect((self.server, self.port))
    #         return self.client.recv(2048).decode()
    #     except:
    #         pass
    



pc = PlayerClient()
print(pc.send("hello"))
print(pc.send("working"))
