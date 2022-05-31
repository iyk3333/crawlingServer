import traceback
import requests


class Payload:
    def __init__(self):
        self.stationInfo = {
            'station': None,
        }



if __name__ == '__main__':
    data = Payload().stationInfo
    data['station'] = "사당역"

    try:
        url = 'http://127.0.0.1:8000/stationInfoModel'
        result = requests.post(url=url, json=data)

        if result.status_code == 200:
            print("success")
        else:
            print("fail")
    except:
        print(traceback.format_exc())

