import requests
from datetime import datetime, timedelta           # datetime 라이브러리안에 있는 datetime와 timedelta 클래스만 호출
import re

# 오늘 날짜 가져오기
"""
date = datetime.now()
date_string = date.strftime('%Y%m%d')
"""

date_string = input("날짜를 입력하세요(입력 형태: YYYYMMDD): ")             # 날짜 입력 받기
date = datetime.strptime(date_string, '%Y%m%d')                            # 입력받은 날짜를 datetime 객체로 변환

weekday = date.weekday()                                                    # 입력받은 날짜의 요일을 구함 (0: 월요일, 6: 일요일)

startday = date - timedelta(days=weekday)                                   # 주의 시작 날짜 (월요일) 계산
stopday = date + timedelta(days=(6-weekday))                                # 주의 끝 날짜 (일요일) 계산

startday = startday.strftime('%Y%m%d')                                      # 시작 날짜를 'YYYYMMDD' 형식의 문자열로 변환
stopday = stopday.strftime('%Y%m%d')                                        # 종료 날짜를 'YYYYMMDD' 형식의 문자열로 변환

day_of_weeks = ['(월)','(화)','(수)','(목)','(금)','(토)','(일)']           # 요일 리스트

url = "https://open.neis.go.kr/hub/mealServiceDietInfo"                     # API 엔드포인트 URL
params = {
    "KEY" : "user_key",                                                             # 인증키
    "Type" : "json",                                                        # 응답 형식
    "pIndex" : 1,                                                           # 페이지 인덱스
    "pSize" : 100,                                                          # 페이지 크기
    "ATPT_OFCDC_SC_CODE" : "D10",                                           # 교육청 코드
    "SD_SCHUL_CODE" : "7240064",                                            # 학교 코드
    # "MLSV_YMD": date_string                                                 # 조회할 날짜
    "MLSV_FROM_YMD" : startday,                                             # 조회 시작 날짜
    "MLSV_TO_YMD" : stopday                                                 # 조회 종료 날짜
}
try:
    response = requests.get(url, params = params)                           # API 요청 보내기
    response.raise_for_status()                                             # HTTP 에러가 발생했는지 확인
except requests.exceptions.RequestException as e:
    print(f"요청 중에 오류가 발생했습니다: {e}")                             # 에러가 발생하면 메시지 출력
else:
    data = response.json()                                                  # 응답 데이터를 JSON 형식으로 변환

    if 'mealServiceDietInfo' in data:
        
        # 데이터 파싱 및 출력
        for item in data['mealServiceDietInfo'][1]['row']:
            day_of_week = day_of_weeks[datetime.strptime(item['MLSV_YMD'], '%Y%m%d').weekday()]  # 날짜의 요일 구하기
            print(item['MLSV_YMD'] + day_of_week + " " + item['MMEAL_SC_NM'])                    # 날짜와 요일, 식사 구분 출력
            menus = item['DDISH_NM'].split('<br/>')                                             # 메뉴 항목을 <br/> 기준으로 분리
            for menu in menus:
                menu = re.sub(r'\(\d+(\.\d+)*\)', '', menu)                                     # 패턴에 매칭되는 부분 제거
                r"""
                \(
                    # 여는 소괄호 '('을 문자 그대로 매칭합니다. 
                    # 소괄호는 정규표현식에서 특별한 의미를 가지므로, 
                    # 문자 그대로 매칭하려면 백슬래시를 사용합니다.
                \d+
                    # 하나 이상의 숫자(digit)를 매칭합니다. 
                    # \d는 0에서 9까지의 숫자를 의미하고, 
                    # +는 하나 이상을 의미합니다.
                (
                    # 소괄호는 그룹을 나타내며, 
                    # 여기서는 점(.)과 숫자(digit)의 반복 패턴을 그룹화합니다.
                    \.
                        # 점(.)을 문자 그대로 매칭합니다. 
                        # 점은 정규표현식에서 임의의 문자 하나를 의미하므로, 
                        # 문자 그대로 매칭하려면 백슬래시를 사용합니다.
                    \d+
                        # 하나 이상의 숫자(digit)를 매칭합니다.
                )*
                    # 앞의 그룹(점과 숫자 패턴)이 0번 이상 반복됨을 의미합니다.
                    # *는 0번 이상 반복을 의미합니다.
                \)
                    # 닫는 소괄호 ')'을 문자 그대로 매칭합니다.
                """
                print("  - " + menu)                                        # 각 메뉴 출력
    else:
        code = data['RESULT']['CODE']                                       # 에러 코드
        message = data['RESULT']['MESSAGE']                                 # 에러 메시지
        print(f"[Error] {code} : {message}")                                # 에러 코드와 메시지 출력
