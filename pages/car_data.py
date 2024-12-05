import streamlit as st
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random
from matplotlib import font_manager, rc
from matplotlib.ticker import FuncFormatter

# 현재 스크립트의 위치가 아닌, 프로젝트 루트를 기준으로 경로 설정
font_path = "fonts/malgun.ttf"  # malgun.ttf 경로
font_manager.fontManager.addfont(font_path)  # 폰트 추가
rc('font', family='Malgun Gothic')  # 폰트 이름 설정

# matplotlib에 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'

# 데이터 로드 및 캐싱
@st.cache_data
def load_data(file_name):
    return pd.read_csv(file_name, encoding="utf-8")

enroll_num = load_data("enrollnum.csv")
enroll_per = load_data("enrollper.csv")
sales_num = load_data("salesnum.csv")
sales_per = load_data("salesper.csv")

# Streamlit 애플리케이션
st.title("전기차 데이터 분석")
option = st.radio("데이터 유형 선택:", ["등록현황", "판매현황"])

if option == "등록현황":
    # 등록 대수 꺾은선 그래프
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for fuel in enroll_num['연료'].unique():
        ax1.plot(enroll_num.columns[4:], enroll_num.loc[enroll_num['연료'] == fuel].values[0][4:], label=fuel)
    ax1.set_title("연료별 연도별 등록 대수")
    ax1.set_xlabel("연도")
    ax1.set_ylabel("등록 대수")
    ax1.legend()
    ax1.yaxis.set_major_locator(MultipleLocator(100000))  # 세로축 간격을 100,000으로 설정

    # 등록 비중 원 그래프
    fig2, ax2 = plt.subplots()
    ax2.pie(enroll_per.iloc[0, 4:], labels=enroll_per.columns[4:], autopct='%1.1f%%')
    ax2.set_title("연료별 등록 비중")

    st.pyplot(fig1)
    st.pyplot(fig2)

elif option == "판매현황":
    # 판매 대수 꺾은선 그래프
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for fuel in sales_num['연료'].unique():
        ax3.plot(sales_num.columns[4:], sales_num.loc[sales_num['연료'] == fuel].values[0][4:], label=fuel)
    ax3.set_title("연료별 연도별 판매 대수")
    ax3.set_xlabel("연도")
    ax3.set_ylabel("판매 대수")
    ax3.legend()
    ax3.yaxis.set_major_locator(MultipleLocator(100000))  # 세로축 간격을 100,000으로 설정
    
    # 판매 비중 원 그래프
    fig4, ax4 = plt.subplots()
    ax4.pie(sales_per.iloc[0, 4:], labels=sales_per.columns[4:], autopct='%1.1f%%')
    ax4.set_title("연료별 판매 비중")

    st.pyplot(fig3)
    st.pyplot(fig4)

# 학습자 질문 섹션
st.subheader("학습자 질문")
q1 = st.text_input("연도별 전기차의 등록현황과 판매현황은 어떠한가요?")
q2 = st.text_input("왜 그런 현상이 나타났을까요? 본인의 생각을 자유롭게 서술해 보세요.")

# 답변 저장 버튼
if st.button("답변 저장"):
    answer_data = {
        "ID": [st.session_state.get("ID", "Unknown")],
        "P1A1": [q1],
        "P1A2": [q2]
    }
    answer_df = pd.DataFrame(answer_data)
    answer_df.to_csv("page1_answer.csv", mode='a', index=False, header=False)
    st.success("답변이 저장되었습니다.")