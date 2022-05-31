import pymongo
from fastapi import FastAPI
from pymongo import MongoClient
from pymongo import errors

import schema
import socket
from util import *



# DB 만들기, index 생성(장소 이름, 장소 주소)
client = MongoClient('127.0.0.1', 27017)
db = client['test1']
placeInfo = db['placeInfo']
reviewInfo = db['reviewInfo']
userInfo = db['userInfo']
# placeInfo.create_index([('placeName', pymongo.ASCENDING), ('placeAddress', pymongo.ASCENDING)], unique=True)
# reviewInfo.create_index([('placeName', pymongo.ASCENDING), ('placeAddress', pymongo.ASCENDING), ('userHash', pymongo.ASCENDING), ('reviewInfoVisitCount', pymongo.ASCENDING)], unique=True)
# userInfo.create_index('userHash', unique=True)

# fastapi, socket 서버
app = FastAPI()

HOST = '127.0.0.1'
PORT = 10229


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))


@app.post('/stationInfoModel')
async def receiveStationInfo(data: schema.stationInfoModel):
    data = dict(data)
    client_socket.send(data['station'].encode('utf-8'))


@app.post('/PlaceInfoModel')
async def receivePlaceInfo(data: schema.PlaceInfoModel):
    print("*" *20 , "장소정보 저장", "*"*20)
    data = dict(data)

    try:
        result = db['placeInfo'].insert_one(data)

    except errors.DuplicateKeyError:
        print("place 정보 이미 있습니다")
        pass
    except Exception as placeError:
        print(traceback.format_exc())
        pass



@app.post('/ReviewInfoModel')
async def receiveReviewInfo(data: schema.ReviewInfoModel):
    data = dict(data)
    # debugPrint(data, mode='first')
    print(data)
    try:
        print("*" * 20, "리뷰정보 저장", "*" * 20)
        result = db['reviewInfo'].insert_one(data)
        # debugPrint(result, mode='insert')
    except errors.DuplicateKeyError:
        print("review 정보 이미 있습니다")
        pass
    except errors.BulkWriteError:
        print(traceback.format_exc())
        pass
    except Exception as reviewError:
        print(traceback.format_exc())
        pass
