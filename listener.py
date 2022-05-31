import socket
import threading
from threading import Thread
from getPlaceListKakao import *
from util import *
from pymongo import MongoClient


# playList API
api = KakaoLocalAPI("a0180dc6fa40d65f96e9a986b26f46c8")

# crawling
hosts = 'http://127.0.0.1:8000'
indexLogPath = 'C:\\Users\\catty\\PycharmProjects\\crawlingServer\\log\\SavedIndex2.log'
errorLogPath = 'C:\\Users\\catty\\PycharmProjects\\crawlingServer\\log\\Noplace2.log'
webdriverPath = 'C:\\Users\\catty\\PycharmProjects\\luckyseven\\crawler\\chromedriver_win32\\chromedriver.exe'
geoLocal = Nominatim(user_agent='South Korea')

# MongoDB
client = MongoClient('127.0.0.1', 27017)
db = client['test1']
placeInfo = db['placeInfo']

# thread lock
lock = threading.Lock()


class Server(Thread):
    def __init__(self):
        super().__init__()
        self.clients = []
        self.host = '127.0.0.1'
        self.port = 10227
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

    def handleConnection(self, client):
        c = Listener(client)
        self.clients.append(c)

    def run(self):
        while True:
            client_socket, addr = self.sock.accept()
            self.handleConnection(client_socket)
            if len(self.clients) != 0:
                lock.acquire()
                self.clients[0].start()
                lock.release()



class Listener(Thread):
    def __init__(self, sock):
        super().__init__()
        self.sock = sock

    def run(self):
        while True:
            # lock.acquire()
            query = self.sock.recv(128).decode('utf-8')
            print("OK")
            placeList = api.getPlaceList(query)
            placeList = findPlaceList(placeList)
            if len(placeList) != 0:
                result = getPlace(placeList)
                print(result)
            # lock.release()


def findPlaceList(placeList):
    print(len(placeList))
    results = []
    for i in placeList:
        result = placeInfo.count_documents({'placeName': i[0], 'placeAddress': i[1]})

        if result == 0:
            results.append({'placeName': i[0], 'placeAddress': i[1]})
    print(len(results))
    # stationInfo.insert_many(results)

    return results


def getPlace(placeList):
    result = []
    util = Util(hosts, indexLogPath, errorLogPath, webdriverPath)
    for place in placeList:
        result.append(util.getPlaceInfoDetails(geoLocal, place['placeName']+place['placeAddress']))
    return result

