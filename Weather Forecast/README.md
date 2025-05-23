# 🌤️ 단기 기상 예보 조회 프로그램

Python을 사용하여 **기상청의 단기예보 데이터를 조회**하는 프로그램입니다.  
[공공데이터포털](https://www.data.go.kr/)의 **기상청_단기예보 ((구)_동네예보) 조회서비스 API**를 활용하며,  
현재 시각을 기준으로 가장 가까운 예보 시간을 계산해 **예보 항목별 날씨 정보를 출력**합니다.

---

## 📌 주요 기능

- 🕑 현재 시각에 맞는 예보 시간 자동 계산
- 📆 기준 날짜(`base_date`) 및 기준 시간(`base_time`) 자동 설정
- ☁️ 기온, 강수, 하늘상태, 풍향/풍속 등 다양한 기상 항목 출력
- 📡 공공데이터 포털 API 실시간 연동
- ⏱️ 예보 시간대별로 정리된 출력

---

## 🔧 사용 방법

1. Python이 설치된 환경에서 아래 파일을 실행하세요:

```bash
python weather_forecast.py
```

2. 실행하면 다음과 같은 형식으로 예보 결과가 출력됩니다:

```
[2025년 04월 10일 14시]
  - 하늘상태(SKY): 1 
  - 1시간 기온(TMP): 16.2 ℃
  - 강수확률(POP): 0 %
  ...
```

> 기상청 API는 3시간 간격으로 예보를 제공하므로, 실행 시점에 가장 가까운 기준 시각의 예보 데이터를 자동으로 선택합니다.

---

## 🗃️ 파일 구성

```plaintext
weather_forecast.py    # 기상청 예보 조회 메인 코드
README.md              # 프로젝트 설명 파일
```

---

## 🧠 학습 포인트

- Python의 `datetime`, `timedelta`를 활용한 시간 계산
- 조건 분기를 통한 동적 기준 시각 설정
- REST API 호출 및 응답(JSON) 처리 (`requests`)
- 예보 카테고리 매핑 및 단위 처리
- 실시간 공공데이터 활용법

---

## 📡 사용 API 정보

- **데이터 출처:** [공공데이터포털](https://www.data.go.kr/)
- **API 명칭:** 기상청_단기예보 ((구)_동네예보) 조회서비스
- **API 문서:** [바로가기](https://www.data.go.kr/data/15084084/openapi.do)

> 사용을 위해서는 공공데이터포털에서 API 키를 발급받아 `serviceKey` 항목에 입력해야 합니다.

---

## 🔑 주의사항

- 이 코드는 실습/학습용으로 작성되었으며, 상업적 이용 시 별도의 허가가 필요할 수 있습니다.
- 공공 API는 호출 제한이 있으므로, 과도한 요청을 피해주세요.

---

## 👨‍💻 개발 정보

- **개발자:** 강준호  
- **이메일:** [junh048@dge.go.kr](mailto:junh048@dge.go.kr)

---

## 📝 참고 및 라이선스

- **데이터 출처:** [공공데이터포털](https://www.data.go.kr/)
  - 기상청_단기예보 ((구)_동네예보) 조회서비스 API
- **문제 발생 시:** 위 이메일로 문의 바랍니다.
- **라이선스:** 본 프로그램은 **비영리 교육용**으로 자유롭게 사용하실 수 있습니다.

---

> 기상청 오픈 API와 Python을 활용해 실시간 데이터를 다루는 실습 예제로,  
> 공공데이터 기반의 자동화 및 데이터 분석 교육에 적합한 프로젝트입니다.
