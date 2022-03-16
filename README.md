# team-local-tactics
A game for the mandatory assignment

Names: Karl Martin Helset, Hannah Mørken, Jonas Holgersen

Run sequence:
It doesn't matter which one of the server or the database you run first as these are equally dependent of eachother. But for the sake of it we would reccommend you to rund the game in this order:

1. Run database_server.py so the database can store Match History and the server can access the database.
2. Run server.py so the clients have something to connect to and the game can run.
3. Run two instances of client.py so they can play against eachother.
4. Run flask_webpage.py so you can se champion stats and match history on a webpage. (You can run this file whenever as it is independent from the other files.) You can find the webpage-address in the terminal. 