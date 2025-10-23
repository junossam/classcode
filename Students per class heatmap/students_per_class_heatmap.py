# -*- coding: utf-8 -*-
"""
Windows 전용: 시도교육청별 학급당 학생수 히트맵

- 폰트: 맑은 고딕
- CSV 인코딩 자동 처리(utf-8-sig 우선, 실패 시 cp949)
- seaborn 있으면 heatmap, 없으면 matplotlib로 대체
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
def set_korean_font_windows():
    # '맑은 고딕'은 대부분의 Windows에 기본 탑재
    plt.rc("font", family="Malgun Gothic")
    # 마이너스 깨짐 방지
    plt.rcParams["axes.unicode_minus"] = False

set_korean_font_windows()

# -----------------------------
# CSV 로더 (인코딩 자동)
# -----------------------------
def read_csv_auto(path: str) -> pd.DataFrame:
    # 우선권: utf-8-sig → 실패 시 cp949
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except Exception:
        return pd.read_csv(path, encoding="cp949")

# -----------------------------
# 전처리
# -----------------------------
def require_columns(df: pd.DataFrame, cols: list, name: str):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{name} 파일에 필요한 컬럼이 없습니다: {missing}")

def load_data():
    data_elem   = read_csv_auto(ELEM_PATH)
    data_middle = read_csv_auto(MIDDLE_PATH)
    data_high   = read_csv_auto(HIGH_PATH)
    return data_elem, data_middle, data_high

def prepare():
    common_columns = ['시도교육청', '교육지원청', '학교명']
    cs_cols_elem = [
        '1학년 학급수', '1학년 학생수',
        '2학년 학급수', '2학년 학생수',
        '3학년 학급수', '3학년 학생수',
        '4학년 학급수', '4학년 학생수',
        '5학년 학급수', '5학년 학생수',
        '6학년 학급수', '6학년 학생수'
    ]
    cs_cols_mh = [
        '1학년 학급수', '1학년 학생수',
        '2학년 학급수', '2학년 학생수',
        '3학년 학급수', '3학년 학생수'
    ]

    data_elem, data_middle, data_high = load_data()
    require_columns(data_elem,   common_columns + cs_cols_elem, "초등")
    require_columns(data_middle, common_columns + cs_cols_mh,   "중등")
    require_columns(data_high,   common_columns + cs_cols_mh,   "고등")

    data_elem_selected   = data_elem[common_columns + cs_cols_elem].copy()
    data_middle_selected = data_middle[common_columns + cs_cols_mh].copy()
    data_high_selected   = data_high[common_columns + cs_cols_mh].copy()

    elem_group_sum   = data_elem_selected.groupby('시도교육청')[cs_cols_elem].sum().reset_index()
    middle_group_sum = data_middle_selected.groupby('시도교육청')[cs_cols_mh].sum().reset_index()
    high_group_sum   = data_high_selected.groupby('시도교육청')[cs_cols_mh].sum().reset_index()
    return elem_group_sum, middle_group_sum, high_group_sum

def calculate_students_per_class_per_school(group_sum_df: pd.DataFrame,
                                            grade_range: range,
                                            start_col_num: int) -> pd.DataFrame:
    df = group_sum_df.copy()
    for g in grade_range:
        stu_col = f"{g+1}학년 학생수"
        cls_col = f"{g+1}학년 학급수"
        val = df[stu_col] / df[cls_col].replace({0: np.nan})
        df[start_col_num + g] = val
    cols = ['시도교육청'] + list(range(start_col_num, start_col_num + len(grade_range)))
    return df[cols]

def build_merged_sorted(elem_group_sum, middle_group_sum, high_group_sum):
    elem_students = calculate_students_per_class_per_school(elem_group_sum,   range(0, 6), 8)
    mid_students  = calculate_students_per_class_per_school(middle_group_sum, range(0, 3), 14)
    high_students = calculate_students_per_class_per_school(high_group_sum,   range(0, 3), 17)

    merged_df = pd.merge(elem_students, mid_students, on='시도교육청', how='inner')
    merged_df = pd.merge(merged_df, high_students, on='시도교육청', how='inner')

    data_order_df = pd.DataFrame({
        '시도교육청': [
            "강원특별자치도교육청", "경기도교육청", "경상남도교육청", "경상북도교육청", "광주광역시교육청",
            "대구광역시교육청", "대전광역시교육청", "부산광역시교육청", "서울특별시교육청", "세종특별자치시교육청",
            "울산광역시교육청", "인천광역시교육청", "전라남도교육청", "전북특별자치도교육청", "제주특별자치도교육청",
            "충청남도교육청", "충청북도교육청"
        ],
        '정렬기준': [15, 9, 10, 11, 3, 2, 4, 5, 1, 8, 6, 7, 12, 16, 17, 13, 14]
    })

    sort_merged_df = pd.merge(merged_df, data_order_df, on='시도교육청', how='left')
    sort_merged_df = sort_merged_df.sort_values(by='정렬기준', kind="mergesort").reset_index(drop=True)
    sort_merged_df = sort_merged_df.drop(columns=['정렬기준'])
    sort_merged_df = sort_merged_df.replace([np.inf, -np.inf], np.nan)
    return sort_merged_df

# -----------------------------
# 히트맵 그리기
# -----------------------------
def draw_heatmap(df: pd.DataFrame):
    heatmap_data = df.set_index('시도교육청').T

    try:
        import seaborn as sns
        plt.figure(figsize=(15, 10))
        ax = sns.heatmap(
            heatmap_data,
            annot=ANNOTATE,
            fmt=ANNOT_FMT,
            cmap=CMAP_NAME,
            cbar_kws={'label': CBAR_LABEL}
        )
        ax.set_title(TITLE)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        ax.set_ylabel(YLABEL)
        plt.tight_layout()
    except Exception:
        # seaborn 없는 경우 matplotlib 대체
        fig, ax = plt.subplots(figsize=(15, 10))
        im = ax.imshow(heatmap_data.values, aspect='auto', cmap=CMAP_NAME)
        ax.set_title(TITLE)
        ax.set_xticks(range(heatmap_data.shape[1]))
        ax.set_yticks(range(heatmap_data.shape[0]))
        ax.set_xticklabels(heatmap_data.columns, rotation=45, ha='right')
        ax.set_yticklabels(heatmap_data.index)
        ax.set_ylabel(YLABEL)

        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label(CBAR_LABEL)

        if ANNOTATE:
            for i in range(heatmap_data.shape[0]):
                for j in range(heatmap_data.shape[1]):
                    v = heatmap_data.iat[i, j]
                    if pd.notna(v):
                        ax.text(j, i, format(v, ANNOT_FMT), ha='center', va='center')

        fig.tight_layout()

    try:
        plt.savefig(SAVE_FIG, dpi=150)
        print(f"[저장완료] {SAVE_FIG}")
    except Exception as e:
        print(f"[저장실패] {e}")
    plt.show()

# -----------------------------
# 메인
# -----------------------------
for p in [ELEM_PATH, MIDDLE_PATH, HIGH_PATH]:
    if not os.path.exists(p):
        print(f"[경고] 파일을 찾을 수 없습니다: {p}")
elem_group_sum, middle_group_sum, high_group_sum = prepare()
sort_merged_df = build_merged_sorted(elem_group_sum, middle_group_sum, high_group_sum)
draw_heatmap(sort_merged_df)