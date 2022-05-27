import json
import traceback

import requests


'''
    참고 코드: https://wooiljeong.github.io/python/kakao_local_api/
    사용 api: http://developer.kakao.com
    
    kakao에서 제공하는 api를 사용하여 역을 입력시 역 주변 1.1km 반경의 음식점을 리스트로 리턴
'''


class KakaoLocalAPI:
    """
    Kakao Local API 컨트롤러
    """

    def __init__(self, rest_api_key):
        """
        Rest API키 초기화 및 기능 별 URL 설정
        """

        # REST API 키 설정
        self.rest_api_key = rest_api_key
        self.headers = {"Authorization": "KakaoAK {key}".format(key=rest_api_key)}

        # 서비스 별 URL 설정

        # 01 주소 검색
        self.URL_01 = "https://dapi.kakao.com/v2/local/search/address.json"
        # 02 좌표-행정구역정보 변환
        self.URL_02 = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
        # 03 좌표-주소 변환
        self.URL_03 = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        # 04 좌표계 변환
        self.URL_04 = "https://dapi.kakao.com/v2/local/geo/transcoord.json"
        # 05 키워드 검색
        self.URL_05 = "https://dapi.kakao.com/v2/local/search/keyword.json"
        # 06 카테고리 검색
        self.URL_06 = "https://dapi.kakao.com/v2/local/search/category.json"



    def search_keyword(self, query, category_group_code=None, x=None, y=None, radius=None, rect=None, page=None,
                       size=None, sort=None) -> set:
        """
        05 키워드 검색
        """
        params = {"query": f"{query}"}


        if category_group_code != None:
            params['category_group_code'] = f"{category_group_code}"
        if x != None:
            params['x'] = f"{x}"
        if y != None:
            params['y'] = f"{y}"
        if radius != None:
            params['radius'] = f"{radius}"
        if rect != None:
            params['rect'] = f"{rect}"
        if page != None:
            params['page'] = f"{page}"
        if size != None:
            params['size'] = f"{params}"
        if sort != None:
            params['sort'] = f"{sort}"

        res = requests.get(self.URL_05, headers=self.headers, params=params)
        document = json.loads(res.text)

        return document

    def getPlaceList(self, query):
        # 중심이 되는 위도, 경도 좌표 가져오기, 중심 좌표에서 1km씩 빼기
        station = self.search_keyword(query=query)
        sx = float(station['documents'][0]['x']) - 0.01
        sy = float(station['documents'][0]['y']) - 0.01


        placeList = set()

        # 중심을 기준으로 1.1km까지 음식점 리스트 찾기, 우측과 아래로 탐색
        for i in range(0, 22):
            for j in range(0, 22):
                nx = sx + 0.001*i
                ny = sy + 0.001*j
                result = self.search_keyword(query=query+"음식점", x=str(nx), y=str(ny), radius=120)

                for k in result['documents']:
                    placeList.add((k['place_name'], k['road_address_name']))
                print(query,"--------->", len(placeList))

        placeList = list(placeList)

        return placeList


# if __name__ == '__main__':
#
#     api = KakaoLocalAPI("a0180dc6fa40d65f96e9a986b26f46c8")
#     place = api.getPlaceList("목동역")
#
#     print(place[0])

