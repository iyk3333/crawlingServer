import argparse
from listener import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--crawlHost', default='http://127.0.0.1:8000', type=str, dest='crawlHost')
    parser.add_argument('--socketHost', default='127.0.0.1', type=str, dest='socketHost')
    parser.add_argument('--socketPort', default=10229, type=int, dest='socketPort')
    parser.add_argument('--mongoHost', default='127.0.0.1', type=str, dest='mongoHost')
    parser.add_argument('--mongoPort', default=27017, type=int, dest='mongoPort')
    parser.add_argument('--kakaoapi', default='a0180dc6fa40d65f96e9a986b26f46c8', type=str, dest='kakaoapi')
    parser.add_argument('--indexLogPath', default='C:\\Users\\catty\\PycharmProjects\\crawlingServer\\log\\SavedIndex2.log', type=str, dest='indexLogPath')
    parser.add_argument('--errorLogPath', default='C:\\Users\\catty\\PycharmProjects\\crawlingServer\\log\\Noplace2.log', type=str, dest='errorLogPath')
    parser.add_argument('--webdriverPath', default='C:\\Users\\catty\\PycharmProjects\\luckyseven\\crawler\\chromedriver_win32\\chromedriver.exe', type=str, dest='webdriverPath')
    parser.add_argument('--user_agent', default='South Korea', type=str, dest='user_agent')
    parser.add_argument('--dbName', default='test1', type=str, dest='dbName')

    args = parser.parse_args()

    indexLogPath = args.indexLogPath
    errorLogPath = args.errorLogPath
    webdriverPath = args.webdriverPath
    crawlHost = args.crawlHost
    socketHost = args.socketHost
    socketPort = args.socketPort
    mongoHost = args.mongoHost
    mongoPort = args.mongoPort
    kakaoapi = args.kakaoapi
    dbName = args.dbName
    user_agent = args.user_agent


    server = Server(crawlHost,socketHost, socketPort, mongoHost, mongoPort, kakaoapi, indexLogPath, errorLogPath, webdriverPath, dbName, user_agent)
    server.start()
