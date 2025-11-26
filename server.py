import socket
from _thread import *
from player import Player
import pickle

server = "127.0.0.1" # server ip (change this when necessary)
port = 4040 # server port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

try:
    s.bind((server, port)) # bind server and port to socket
except socket.error as e: # if binding fails
    str(e)

    #listening for a connection
s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0
# def read_pos(str):
#     str = str.split(",")
#     return int(str[0]), int(str[1])

# def make_pos(tup):
#     return str(tup[0]) + "," + str(tup[1])

#pos = [(0,0), (100, 100)]

# players = [Player(0, 0, 50, 50, (255, 0, 0)),
#            Player(100, 100, 50, 50, (0, 0, 255))]

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p))) # alert the user of a connection

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

    while True:
        conn, addr = s.accept()
        print("Connected to:", addr)

        idCount += 1
        p = 0
        gameId = (idCount - 1)//2
        if idCount % 2 == 1:
            games[gameId] = Game(gameId)
            print("Creating a new game...")
        else:
            game(gameId).ready = True
            p = 1

        start_new_thread(threaded_client, (conn, p , gameId))

        #     players[player] = data

        #     if not data:
        #         print("Disconnected") # if no data transferred during the loop, assume there's a disconnection
        #         break
        #     else:
        #         if player == 1:
        #             reply = players[0]
        #         else:
        #             reply = players[1]
                
        #         print("Received: ", reply) # if data, print to console.
        #         print("Sending : ", reply)

        #     conn.sendall(pickle.dumps(reply))
        # except:
        #     break

    print("Lost connection") # tell the user connection is lost
    conn.close() # if lost, close the connection down


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,currentPlayer))
    currentPlayer += 1
