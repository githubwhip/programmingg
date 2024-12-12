import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Streamlit 애플리케이션 시작
st.title("차종별 연도별 등록 현황")

# 사용자 입력: 차종 선택
vehicle_types = enroll_num['구분'].unique()
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종에 대한 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]

# 등록 대수 꺾은선 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))

# 그래프 그리기
ax.plot(selected_num_data['연도'], selected_num_data['등록 대수'], marker='o')
ax.set_title(f"{selected_vehicle} 연도별 등록 대수")
ax.set_xlabel("연도")
ax.set_ylabel("등록 대수")

# 세로축 숫자 레이블 제거
ax.set_yticklabels([])

# 데이터 포인트에 숫자 레이블 추가
for i, txt in enumerate(selected_num_data['등록 대수']):
    ax.annotate(f'{int(txt):,}', (selected_num_data['연도'].iloc[i], txt), textcoords="offset points", xytext=(0, 10), ha='center')

# 그래프 출력
st.pyplot(fig)
