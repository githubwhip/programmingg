import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(file_name):
    df = pd.read_csv(file_name, encoding="utf-8")
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거
    return df

def preprocess_data(df, value_name):
    df = df[~df['구분'].isin(['합계', '기타'])].reset_index(drop=True)
    df = df.iloc[:, 3:]  # '구분' 열부터 시작하도록 조정
    df = df.melt(id_vars=["구분"], var_name="연도", value_name=value_name)
    if "대수" in value_name:
        df[value_name] = df[value_name].str.replace(",", "").astype(float)
    elif "비중" in value_name:
        df[value_name] = df[value_name].str.replace("%", "").astype(float)
    return df

# 데이터 로드 및 전처리
enroll_num = preprocess_data(load_data("enrollnum.csv"), "등록 대수")
enroll_per = preprocess_data(load_data("enrollper.csv"), "등록 비중")

# 각 차종별 최대값과 최소값 계산하여 y축 스케일 결정
def calculate_y_axis_scale(df):
    scales = {}
    for _, row in df.iterrows():
        vehicle = row['구분']
        vehicle_data = row.iloc[1:]  # 연도별 데이터만 선택
        min_value = vehicle_data.min()
        max_value = vehicle_data.max()
        range_value = max_value - min_value
        if range_value <= 500000:
            scale = 100000  # 10만 단위
        elif range_value <= 2000000:
            scale = 500000  # 50만 단위
        else:
            scale = 1000000  # 100만 단위
        scales[vehicle] = {'min': min_value, 'max': max_value, 'scale': scale}
    return scales

scales = calculate_y_axis_scale(enroll_num)

# Streamlit 애플리케이션 시작
st.title("차종별 연도별 등록 현황")

# 사용자 입력: 차종 선택
vehicle_types = enroll_num['구분'].unique()
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종에 대한 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]
selected_per_data = enroll_per[enroll_per['구분'] == selected_vehicle]

# 등록 대수 꺾은선 그래프 생성 (세로축 백만 단위 설정)
fig1, ax1 = plt.subplots(figsize=(10, 6))

# 그래프 그리기
ax1.plot(selected_num_data['연도'], selected_num_data['등록 대수'], marker='o')
ax1.set_title(f"{selected_vehicle} 연도별 등록 대수")
ax1.set_xlabel("연도")
ax1.set_ylabel("등록 대수")

# 세로축을 적절한 단위로 설정 (지수 표기 제거)
vehicle_scale_info = scales[selected_vehicle]
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x / vehicle_scale_info["scale"])}M'))
ax1.set_ylim(vehicle_scale_info['min'], vehicle_scale_info['max'])

# 숫자 레이블 추가
for i, txt in enumerate(selected_num_data['등록 대수']):
    ax1.annotate(f'{int(txt):,}', (selected_num_data['연도'].iloc[i], txt), textcoords="offset points", xytext=(0,10), ha='center')

# 등록 비중 막대 그래프 생성 (가로 방향)
fig2, ax2 = plt.subplots(figsize=(10, 6))
colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(selected_per_data))]
ax2.barh(selected_per_data['연도'], selected_per_data['등록 비중'], color=colors)
ax2.set_title(f"{selected_vehicle} 연도별 등록 비중")
ax2.set_xlabel("등록 비중 (%)")
ax2.set_ylabel("연도")

# 퍼센트 레이블 추가
for i, v in enumerate(selected_per_data['등록 비중']):
    ax2.text(v, i, f'{v:.1f}%', va='center', ha='left')

# 그래프 출력
st.pyplot(fig1)
st.pyplot(fig2)
