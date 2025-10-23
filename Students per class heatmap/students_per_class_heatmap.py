import os
import pandas as pd                         # 판다스 라이브러리 호출
import numpy as np
import matplotlib.pyplot as plt             # 그래프 생성 라이브러리 호출
import seaborn as sns                       # 히트맵 사용을 위해 필요한 라이브러리 호출

# -----------------------------
# 경로 설정 (필요시 수정)
# -----------------------------
ELEM_PATH   = "./2025_Grade_Class_Elem.csv"
MIDDLE_PATH = "./2025_Grade_Class_Middle.csv"
HIGH_PATH   = "./2025_Grade_Class_High.csv"
SAVE_FIG    = "./시도교육청별_학급당_학생수_히트맵.png"

TITLE       = "시도교육청별 학급당 학생수 히트맵"
CBAR_LABEL  = "학급당 학생수"
YLABEL      = "학년"   # 원 코드의 '나이' 대신 '학년'이 더 적합
CMAP_NAME   = "YlGnBu"
ANNOTATE    = True
ANNOT_FMT   = ".2f"

# -----------------------------
# Windows 한글 폰트 설정
# -----------------------------
# '맑은 고딕'은 대부분의 Windows에 기본 탑재
plt.rc("font", family="Malgun Gothic")
# 마이너스 깨짐 방지
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------
# CSV 로더 (인코딩 자동)
# -----------------------------
# 초등학교 엑셀 파일 전체 읽기
file_elem = './2025_Grade_Class_Elem.csv'
data_elem = pd.read_csv(file_elem)

# 중학교 엑셀 파일 전체 읽기
file_middle = './2025_Grade_Class_Middle.csv'
data_middle = pd.read_csv(file_middle)

# 고등학교 엑셀 파일 전체 읽기
file_high = './2025_Grade_Class_High.csv'
data_high = pd.read_csv(file_high)

# -----------------------------
# 전처리(필요한 컬럼만 선택)
# -----------------------------
# 공통 컬럼 정의
common_columns = ['시도교육청', '교육지원청', '학교명']

# 초등학교 (1학년 ~ 6학년) 컬럼
cs_cols_elem = ['1학년 학급수', '1학년 학생수', '2학년 학급수', '2학년 학생수', '3학년 학급수', '3학년 학생수',
                '4학년 학급수', '4학년 학생수', '5학년 학급수', '5학년 학생수', '6학년 학급수', '6학년 학생수']
columns_elem = common_columns + cs_cols_elem
print(columns_elem)

# 중학교 및 고등학교 (1학년 ~ 3학년) 컬럼
cs_cols_mh = ['1학년 학급수', '1학년 학생수', '2학년 학급수', '2학년 학생수', '3학년 학급수', '3학년 학생수']
columns_mh = common_columns + cs_cols_mh
print(columns_mh)

# 지정된 컬럼만 선택
data_elem_selected = data_elem[columns_elem]
data_middle_selected = data_middle[columns_mh]
data_high_selected = data_high[columns_mh]

# -----------------------------
# 전처리(결측치 처리리)
# -----------------------------
# 결측치 확인
print("초등학교 열별 결측치 개수")
print(data_elem_selected.isnull().sum())

print()

print("중학교 열별 결측치 개수")
print(data_middle_selected.isnull().sum())

print()

print("고등학교 열별 결측치 개수")
print(data_high_selected.isnull().sum())

# 결측치가 없으므로 추가 작업 하지 않음

# -----------------------------
# 데이터 처리(학급수, 학생수를 그룹별로 합계구하기)
# 반별 인원수 데이터로 평균을 구하면 데이터 외곡 발생으로 학급수, 학생수를 따로 구한 후 직접 나눠서 평균 계산
# -----------------------------
# 초등학교 시도교육청 기준 합계 계산
elem_group_sum = data_elem_selected.groupby('시도교육청')[cs_cols_elem].sum()
elem_group_sum = elem_group_sum.reset_index()

# 중학교 시도교육청 기준 합계 계산
middle_group_sum = data_middle_selected.groupby('시도교육청')[cs_cols_mh].sum()
middle_group_sum = middle_group_sum.reset_index()

# 고등학교 시도교육청 기준 합계 계산
high_group_sum = data_high_selected.groupby('시도교육청')[cs_cols_mh].sum()
high_group_sum = high_group_sum.reset_index()

# 학생수 / 학급수 함수 생성
def calculate_students_per_class(data):
    return data[0] / data[1]

# 학급당 학생수 구하기기
def calculate_students_per_class_per_school(school_group_sum_df, grade_range, start_col_num):
    for grade in grade_range:
        selected_columns = [f'{grade+1}학년 학생수', f'{grade+1}학년 학급수']
        school_group_sum_df[start_col_num + grade] = school_group_sum_df[selected_columns].apply(calculate_students_per_class, axis=1)

    # 학년별 결과 컬럼과 시도교육청 컬럼만 선택
    columns_to_select = ['시도교육청'] + list(range(start_col_num, start_col_num + len(grade_range)))
    return school_group_sum_df[columns_to_select]


# 초등학교 학급당 학생 수 계산
elem_students_per_class_df = calculate_students_per_class_per_school(elem_group_sum, range(0, 6), 8)

# 중학교 학급당 학생 수 계산
middle_students_per_class_df = calculate_students_per_class_per_school(middle_group_sum, range(0, 3), 14)

# 고등학교 학급당 학생 수 계산
high_students_per_class_df = calculate_students_per_class_per_school(high_group_sum, range(0, 3), 17)


# -----------------------------
# 데이터 합치기
# -----------------------------
merged_df = pd.merge(elem_students_per_class_df, middle_students_per_class_df,
                     on='시도교육청',
                     how='inner')
merged_df = pd.merge(merged_df, high_students_per_class_df,
                     on='시도교육청',
                     how='inner')


# -----------------------------
# 지정된 지역순으로 데이터 정렬 수행
# -----------------------------
# 정렬 순서와 데이터 이름을 포함하는 데이터프레임 생성
data_order_df = pd.DataFrame({
    '시도교육청': ["강원특별자치도교육청", "경기도교육청", "경상남도교육청", "경상북도교육청", "광주광역시교육청",
                   "대구광역시교육청", "대전광역시교육청", "부산광역시교육청", "서울특별시교육청", "세종특별자치시교육청",
                   "울산광역시교육청", "인천광역시교육청", "전라남도교육청", "전북특별자치도교육청", "제주특별자치도교육청",
                   "충청남도교육청", "충청북도교육청"
                   ],
    '정렬기준': [15, 9, 10, 11, 3,
                2, 4, 5, 1, 8,
                6, 7, 12, 16, 17,
                13, 14
                ]
})

sort_merged_df = pd.merge(merged_df, data_order_df, on='시도교육청')
sort_merged_df = sort_merged_df.sort_values(by='정렬기준').reset_index(drop=True)
sort_merged_df = sort_merged_df.drop(columns='정렬기준')
print(sort_merged_df)

# -----------------------------
# 히트맵 그리기
# -----------------------------
# 히트맵을 위한 데이터 준비
heatmap_data = sort_merged_df.set_index('시도교육청').T          # .T 행열 바꿈

plt.figure(figsize=(15, 10))
sns.heatmap(
    heatmap_data,             # 데이터
    annot=True,               # 셀에 데이터 값 표시
    fmt=".2f",                # 데이터 값 형식
    cmap="YlGnBu",            # 색상 맵
    cbar_kws={'label': '학급당 학생수'}  # 컬러바 속성
)
plt.title('시도교육청별 학급당 학생수 히트맵')
plt.xticks(
    rotation=45,            # 레이블 기울기
    ha='right'              # ha='left/right/center' 레이블 정렬 기준
)
plt.yticks(rotation=0)      # y축 눈금 레이블의 회전 각도
plt.ylabel('나이')          # y축에 '나이'라는 제목을 추가
plt.savefig(SAVE_FIG, dpi=150)
plt.show()
