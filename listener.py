import socket
from threading import Thread
from getPlaceListKakao import *
from util import *
from pymongo import MongoClient


def findPlaceList(nameList, addressList, placeList, placeInfo):
    placeInfo = list(placeInfo)

    placeInfo.aggregate([
        {'$project': {'index': {'$concat': ["$placeName", "$placeAddress"]}}},
        {'$merge': 'placeInfo'}
    ])
    result = placeInfo.find({'index': {'$in': placeList}})


    alreadyList = list()
    for i in result:
        print(i)
        alreadyList.append((i['placeName'], i['placeAddress']))

    results = set(placeList) - set(alreadyList)
    # print(len(results))

    return list(results)


def getPlace(placeList, crawlHost, indexLogPath, errorLogPath, webdriverPath, geoLocal):
    result = []
    util = Util(crawlHost, indexLogPath, errorLogPath, webdriverPath)
    for place in placeList:
        util.getPlaceInfoDetails(geoLocal, place[0]+place[1])


class Server(Thread):
    def __init__(self,crawlHost, socketHost, socketPort, mongoHost, mongoPort, kakaoapi, indexLogPath, errorLogPath, webdriverPath, dbName, user_agent):
        super().__init__()
        self.clients = []
        self.crawlHost = crawlHost
        self.host = socketHost
        self.port = socketPort
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        self.mongoHost = mongoHost
        self.mongoPort = mongoPort
        self.kakaoapi = kakaoapi
        self.indexLogPath = indexLogPath
        self.errorLogPath = errorLogPath
        self.webdriverPath = webdriverPath
        self.dbName = dbName
        self.user_agent = user_agent

    def handleConnection(self, client):
        c = Listener(client, self.kakaoapi, self.mongoHost, self.mongoPort, self.dbName, self.crawlHost, self.user_agent, self.indexLogPath, self.errorLogPath, self.webdriverPath)
        c.start()
        self.clients.append(c)

    def run(self):
        while True:
            client_socket, addr = self.sock.accept()
            self.handleConnection(client_socket)




class Listener(Thread):
    def __init__(self, sock, kakaoapi, host, port, dbName, crawlHost, user_agent, indexLogPath, errorLogPath, webdriverPath):
        super().__init__()
        self.sock = sock
        self.api = KakaoLocalAPI(kakaoapi)
        self.client = MongoClient(host, port)
        self.db = self.client[dbName]
        self.placeInfo = self.db['placeInfo']
        self.crawlHost = crawlHost
        self.geoLocal = Nominatim(user_agent=user_agent)
        self.indexLogPath = indexLogPath
        self.errorLogPath = errorLogPath
        self.webdriverPath = webdriverPath


    def run(self):
        while True:
            query = self.sock.recv(128).decode('utf-8')
            nameList, addressList, placeList = self.api.getPlaceList(query)
            placeList = findPlaceList(nameList, addressList, placeList, self.placeInfo)
            if len(placeList) != 0:
                getPlace(placeList, self.crawlHost, self.indexLogPath, self.errorLogPath, self.webdriverPath, self.geoLocal)


