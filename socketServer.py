# import socket
# from _thread import *
# from threading import Thread
# from util import *
# from getPlaceListKakao import *
#
# clients = []
# host = '127.0.0.1'
# port = 13125
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# sock.bind((host, port))
# sock.listen()
#
# api = KakaoLocalAPI("a0180dc6fa40d65f96e9a986b26f46c8")
# hosts = 'http://127.0.0.1:8000'
#
# # 로그 파일 & 웹드라이버 경로
# indexLogPath = 'C:\\Users\\catty\\PycharmProjects\\crawlingServer\\log\\SavedIndex2.log'
# errorLogPath = 'C:\\Users\\catty\\PycharmProjects\\crawlingServer\\log\\Noplace2.log'
# webdriverPath = 'C:\\Users\\catty\\PycharmProjects\\luckyseven\\crawler\\chromedriver_win32\\chromedriver.exe'
#
# geoLocal = Nominatim(user_agent='South Korea')
#
#
#
# def threaded(client_socket, addr):
#     while True:
#         query = client_socket.recv(1024).decode('utf-8')
#         # 장소 리스트 가져오기
#         placeList = api.getPlaceList(query)
#
#         # 크롤링
#         # util = Util(hosts, indexLogPath, errorLogPath, webdriverPath)
#         # result = util.getPlaceInfoDetails(geoLocal, placeList)
#         # print(result)
#         break
#     client_socket.close()
#
# try:
#     while True:
#         client_socket, addr = sock.accept()
#         clients.append(client_socket)
#         start_new_thread(threaded, (client_socket, addr))
#
#
# except Exception as e:
#     print("ERROR: ", e)
#
# finally:
#     sock.close()

from listener import *

server = Server()
server.start()
