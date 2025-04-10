import requests
from datetime import datetime

now = datetime.now()                                            # 현재 날짜와 시간을 가져옴

if now.hour < 2 or (now.hour == 2 and now.minute < 10):
    base_date = now - datetime.timedelta(days=1)                # 현재 시간이 2시 10분 이전이면 날짜를 하루 전으로 설정
else:
    base_date = now                                             # 그렇지 않으면 현재 날짜를 사용
base_date = base_date.strftime('%Y%m%d')                        # 날짜를 'YYYYMMDD' 형식의 문자열로 변환

times = [2, 5, 8, 11, 14, 17, 20, 23]                           # 기상청 API에서 제공하는 예보 시간 목록
adjusted_hour = now.hour - int(now.minute < 10)                 # 현재 시간이 10분 이전이면 시간을 1시간 전으로 조정
possible_times = []                                             # 가능한 예보 시간 목록을 저장할 리스트

for time in times:
    if time <= adjusted_hour:
        possible_times.append(time)                             # 조정된 시간보다 이전인 예보 시간을 추가

if possible_times:
    base_time = max(possible_times)                             # 가능한 예보 시간 중 가장 최근 시간을 선택
else:
    base_time = 23                                              # 가능한 예보 시간이 없으면 23시로 설정

base_time = f'{base_time:02d}00'                                # 예보 시간을 'HH00' 형식의 문자열로 변환

url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"  # API 엔드포인트 URL
params = {
    "serviceKey": "user_key_Decoding",                                           # 서비스 키
    "dataType": "json",                                         # 응답 형식
    "numOfRows": "48",                                          # 한 페이지 결과 수
    "base_date": base_date,                                     # 기준 날짜
    "base_time": base_time,                                     # 기준 시간
    "nx": "90",                                                 # X 좌표
    "ny": "90"                                                  # Y 좌표
}

response = requests.get(url, params=params)                     # API 요청 보내기

data = response.json()                                          # 응답 데이터를 JSON 형식으로 변환

old_time = ""                                                   # 이전 시간 저장 변수

category_dict = {                                               # 카테고리와 단위 정보를 저장하는 딕셔너리
    "POP": ("강수확률", "%"),
    "PTY": ("강수형태", ""),
    "PCP": ("1시간 강수량", ""),
    "REH": ("습도", "%"),
    "SNO": ("1시간 신적설", ""),
    "SKY": ("하늘상태", ""),
    "TMP": ("1시간 기온", "℃"),
    "TMN": ("일 최저기온", "℃"),
    "TMX": ("일 최고기온", "℃"),
    "UUU": ("풍속(동서성분)", "m/s"),
    "VVV": ("풍속(남북성분)", "m/s"),
    "WAV": ("파고", "M"),
    "VEC": ("풍향", "deg"),
    "WSD": ("풍속", "m/s"),
}

items = data['response']['body']['items']['item']               # 예보 항목 리스트
for item in items:
    # print(f"[{item['fcstDate']} {item['fcstTime']}] {item['category']}: {item['fcstValue']}")
    new_time = item['fcstDate'] + item['fcstTime']              # 예보 날짜와 시간을 결합
    if old_time != new_time:                                    # 이전 시간과 현재 시간이 다르면 새로운 시간으로 변경
        date_time_obj = datetime.strptime(new_time, '%Y%m%d%H%M')                       # 문자열을 datetime 객체로 변환
        formatted_date_time = date_time_obj.strftime('%Y년 %m월 %d일 %H시')             # 원하는 형식으로 변환
        print("[" + formatted_date_time + "]")                  # 변환된 시간 출력
        old_time = new_time                                     # 이전 시간을 현재 시간으로 갱신
    category_name, unit = category_dict[item['category']]                               # 카테고리 이름과 단위 가져오기
    print(f"  - {category_name}({item['category']}): {item['fcstValue']} {unit}")       # 예보 정보 출력
