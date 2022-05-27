from fastapi import FastAPI
import schema
import listener
import socket


app = FastAPI()
server = listener.Server()
server.start()


@app.post('/placeInfoModel')
async def receivePlaceInfo(data: schema.placeInfoModel):
    data = dict(data)


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 10000))     # 접속할 서버의 ip주소와 포트번호를 입력.
    result = sock.send(data['station'].encode())
