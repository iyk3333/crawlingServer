import threading
from threading import Thread
import socket
from getPlaceList import *

index = 0

class Server(Thread):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.host = '127.0.0.1'
        self.port = 10000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def handleConnection(self, client, addr):
        c = Listener(client)
        c.start()
        self.clients.append(c)

    def run(self):
        while True:
            client_socket, client_addr = self.sock.accept()
            self.handleConnection(client_socket, client_addr)

            thread = threading.Thread(target=self.handleConnection, args=(client_socket, client_addr))
            thread.daemon = True
            thread.start()

    # def work(self):
    #     while True:
    #         if len(self.clients) != 0:
    #             c = self.clients[0]
    #             del self.clients[0]
    #             c.start()


class Listener(Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        message = self.sock.recv(128).decode('utf-8')

        api = KakaoLocalAPI("a0180dc6fa40d65f96e9a986b26f46c8")
        place = api.getPlaceList(message)

        print(message, " ", place[0])
        # print(message)
