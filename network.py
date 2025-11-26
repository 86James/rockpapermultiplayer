import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1" # ip address
        self.port = 4040 # port
        self.addr = (self.server, self.port) # make the address for server and port
        self.p = self.connect()
        #self.id = self.connect() # assign an id to whatever connects to the client
        #print(self.id)

    def getP(self):
        return self.p

    def connect(self):
        # this try except statement tires to connect, or pass over if it can't.
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
        
    def send(self, data):
        # allows us to send back information when we connecte
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)