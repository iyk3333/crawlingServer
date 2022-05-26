from fastapi import FastAPI
import schema


app = FastAPI()



@app.post('/placeInfoModel')
async def receivePlaceInfo(data: schema.placeInfoModel):
    print(data)