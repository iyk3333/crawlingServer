# # 네이버 검색 API예제는 블로그를 비롯 전문자료까지 호출방법이 동일하므로 blog검색만 대표로 예제를 올렸습니다.
# # 네이버 검색 Open API 예제 - 블로그 검색
# import os
# import sys
# import urllib.request
#
# def getPlaceInfo():
#     client_id = "DpSDdXesQSkH8xftnxC1"
#     client_secret = "sAXJc9T_aI"
#     encText = urllib.parse.quote("브레드박스 목동점")
#     url = "https://openapi.naver.com/v1/search/local?query=" + encText # json 결과
#     request = urllib.request.Request(url)
#     request.add_header("X-Naver-Client-Id",client_id)
#     request.add_header("X-Naver-Client-Secret",client_secret)
#     response = urllib.request.urlopen(request)
#     rescode = response.getcode()
#     if(rescode==200):
#         response_body = response.read()
#         print(response_body.decode('utf-8'))
#     else:
#         print("Error Code:" + rescode)
#
# getPlaceInfo()


import requests
import urllib, openpyxl, time

def placeInfo():
    # place = ['오늘은 지은다방', '장군집', '목동버거', '유진참치', '강고집해물품은찜', '원할머니보쌈족발 신정점']
    place = ['목동역 음식점']
    places = []
    for i in place:
        keyword = i

        url_keyword = urllib.parse.quote(keyword)

        try:

            for p in range(1, 45):
                response = requests.get(
                    f'https://map.naver.com/v5/api/search?caller=pcweb&query={url_keyword}&type=all&page={p}&displayCount=10&lang=ko',
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}).json()

                numbers = response['result']['place']['list']
                # print(numbers[0])

                for i in range(0, len(numbers)):
                    name = response['result']['place']['list'][i]['name']

                    address = response['result']['place']['list'][i]['roadAddress']

                    tel = response['result']['place']['list'][i]['telDisplay']

                    menuinfo = response['result']['place']['list'][i]['menuInfo']

                    description = response['result']['place']['list'][i]['description']
                    link = response['result']['place']['list'][i]['link']

                    # print(name, address, tel, menuinfo)
                    print(link)

                    places.append([name, address, tel, menuinfo])

                time.sleep(1)

        except:
            print('끝났습니다.')

    return places


result = placeInfo()
print(len(result))
