import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import koreanize_matplotlib
from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager, rc

# 폰트 설정
font_path = "fonts/malgun.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_data(file_name):
    df = pd.read_csv(file_name, encoding="utf-8")
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거
    return df

def preprocess_data(df, value_name):
    df = df.dropna(subset=['구분']).reset_index(drop=True)  # NaN 제거
    df = df.melt(id_vars=["구분"], var_name="연도", value_name=value_name)
    if "대수" in value_name:
        df[value_name] = df[value_name].str.replace(",", "").astype(float)
    elif "비중" in value_name:
        df[value_name] = df[value_name].str.replace("%", "").astype(float)
    return df

# 데이터 로드 및 전처리
sales_num = preprocess_data(load_data("salesnumb.csv"), "판매 대수")
sales_per = preprocess_data(load_data("salesperc.csv"), "판매 비중")  # 판매 비중 데이터 추가

# Streamlit 애플리케이션 시작
st.title("차종별 연도별 판매 현황")

# 사용자 입력: 차종 선택
vehicle_types = sales_num['구분'].unique()
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종에 대한 데이터 필터링
selected_num_data = sales_num[sales_num['구분'] == selected_vehicle]
selected_per_data = sales_per[sales_per['구분'] == selected_vehicle]

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)

with col1:
    # 판매 대수 꺾은선 그래프 생성
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    # 그래프 그리기
    ax1.plot(selected_num_data['연도'], selected_num_data['판매 대수'], marker='o')
    ax1.set_title(f"{selected_vehicle} 연도별 판매 대수")
    ax1.set_xlabel("연도")
    ax1.set_ylabel("판매 대수")
    
    # 세로축 숫자 레이블 제거
    ax1.set_yticklabels([])

    # 데이터 포인트에 숫자 레이블 추가
    for i, txt in enumerate(selected_num_data['판매 대수']):
        ax1.annotate(f'{int(txt):,}', (selected_num_data['연도'].iloc[i], txt), textcoords="offset points", xytext=(0, 10), ha='center')

    # 그래프 출력
    st.pyplot(fig1)

with col2:
    # 판매 비중 막대 그래프 생성 (가로 방향)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(selected_per_data))]
    
    ax2.barh(selected_per_data['연도'], selected_per_data['판매 비중'], color=colors)
    ax2.set_title(f"{selected_vehicle} 연도별 판매 비중")
    ax2.set_xlabel("판매 비중 (%)")
    ax2.set_ylabel("연도")

    # 퍼센트 레이블 추가
    for i, v in enumerate(selected_per_data['판매 비중']):
        ax2.text(v, i, f'{v:.1f}%', va='center', ha='left')

    # 그래프 출력
    st.pyplot(fig2)

# 학습지 섹션 추가
st.header("학습지")

# 질문 1
answer_1 = st.text_input("1. 하이브리드 차 판매 대수를 볼 때, 꺾은선 그래프의 눈금을 어떻게 표기하면 좋을까요? \n(예: 100,000부터 시작하여 10만 단위 간격으로 표시 등)")

# 질문 2
answer_2 = st.text_input("2. 연도별 판매 대수와 판매 비중이 가장 높은 차종은 어떤 것인가요? \n(예: 수소 등)")

# 질문 3
answer_3 = st.text_input("3. 시간이 흐름에 따라 판매 대수와 판매 비중이 증가하는 차종은 어떤 것인가요? \n(예: 휘발유 등)")

# 질문 4
answer_4 = st.text_area("4. 여러분이 판매현황을 조작해보면서 느낀 점, 알게된 점, 궁금한 점 등을 자유롭게 서술해 주세요.")
