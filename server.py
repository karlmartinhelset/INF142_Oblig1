import socket
import pickle
from core import Match, Team
from database_server import DBHandler


class server:
    
    def __init__(self):
        self.host = 'localhost'
        self.port = 5550
        self.connections = []
        self.team1 = []
        self.team2 = []
        
        # create socket and bind it to host and port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        
        # start listening to messages
        self.sock.listen()
        
        print("Waiting for players to start game")
        
        # get connections
        self.accept_conn()

        # close socket
        self.sock.close()
        print("Server is closed")


    def accept_conn(self):
        while True:
            conn, _ = self.sock.accept()
            
            self.connections.append(conn)

            # if there is only one client connected to server, wait for another
            if(len(self.connections) == 1):
                msg = ("Waiting", "Waiting for other player ...")
                self.connections[0].send(pickle.dumps(msg))

            # two clients connected. The game can run    
            else:
                self.run_game()
                break


    def send_everyone(self, message):
        for connection in self.connections:
            connection.send(pickle.dumps(message))
            

    def get_players(self, nr):
        if nr == 1:
            msg = ("Choose player",f"Player {nr}" ,"red", self._champions, self.team1, self.team2)
            # Which index the player has in the self.connections-list
            indx = 0

        elif nr == 2:
            msg = ("Choose player", f"Player {nr}", "blue", self._champions, self.team1, self.team2)
            indx = 1

        # send info about the player to the players client
        self.connections[indx].send(pickle.dumps(msg))

        # players are chosen in the clients

        while True:
            # fetch the chosen player
            champ = self.connections[indx].recv(1024).decode()

            if not champ:
                continue
            
            # adds the player to the right team
            if nr == 1:
                self.team1.append(champ)
            else:
                self.team2.append(champ)
            break


    def run_game(self):
        msg = ("Welcome", '\n'
                'Welcome to [bold yellow]Team Local Tactics[/bold yellow]!'
                '\n'
                'Each player choose a champion each time.'
                '\n')
        # send welcome message to each client
        self.send_everyone(msg)
        
        # create new DBHandler-object
        DB = DBHandler()
        
        # fetch champions from database
        self._champions = DB.get_champs()

        # send chamions to client, where a table to show the stats is created
        msg = ("Get champs", self._champions)
        self.send_everyone(msg)

        # get players 
        # two players on each team
        for _ in range(2):
            self.get_players(1)
            self.get_players(2)

        # create match from the match class with the two teams
        match = Match(
                Team([self._champions[name] for name in self.team1]),
                Team([self._champions[name] for name in self.team2])
            )

        # play match
        match.play()

        # get match result from client
        msg = ("Print match", match)
        self.send_everyone(msg)

        # upload match result to database
        DB.add_new_match(match.to_dict())


if __name__ == "__main__":
    servr = server()
    
