import socket
import pickle
from core import Match, Team
from DBHandler import DBHandler

class server:
    
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.connections = []
        self.team1 = []
        self.team2 = []

    def turn_on(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        
        self.DB_sock = socket.create_connection((self.host, 7020))
        
        self.sock.listen()
        print("Looking for connection")
        self.accept_conn()


    def turn_off(self):
        self.sock.close()
        print("Server is closed")


    def accept_conn(self):
        while True:
            conn, _ = self.sock.accept()
            
            self.connections.append(conn)

            if(len(self.connections) == 1):
                data = ("Waiting", "Waiting for other player")
                self.connections[0].send(pickle.dumps(data))
                
            else:
                self.run_game()


    def send_everyone(self, message):
        for connection in self.connections:
            connection.send(pickle.dumps(message))
            

    def get_team(self, nr):
        if nr == 1:
            data = ("Choose player",f"Player {nr}" ,"red", self._champions, self.team1, self.team2)
            choosingIndex = 0

        else:
            data = ("Choose player", f"Player {nr}", "blue", self._champions, self.team1, self.team2)
            choosingIndex = 1

        self.connections[choosingIndex].send(pickle.dumps(data))

        while True:
            champ = self.connections[choosingIndex].recv(1024).decode()

            if not champ:
                continue
            
            if nr == 1:
                self.team1.append(champ)
            else:
                self.team2.append(champ)
            break


    def run_game(self):
        data = ("Welcome", '\n'
                'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
                '\n'
                'Each player choose a champion each time.'
                '\n')
        # send message to each client
        self.send_everyone(data)
        
        DB = DBHandler(self.host, self.port)

        # fetch champions from database
        self._champions = DB.get_champs()

        # create a table containing the champions
        data = ("Get champs", self._champions)
        
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
                Team([self._champions[name] for name in self.team1]),
                Team([self._champions[name] for name in self.team2])
            )
        # play match
        match.play()

        # get match result from team_local_tactics.print_match_summary(match)
        data = ("Print match", match)
        
        # send result to client
        self.send_everyone(data)

        # upload match result to database
        DB.add_new_match(match.to_dict())


if __name__ == "__main__":
    #host = socket.gethostbyname(socket.gethostname())
    host = 'localhost'
    port = 5550
    servr = server(host, port)
    servr.turn_on()
    servr.turn_off()
    
