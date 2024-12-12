import streamlit as st
import pandas as pd
import koreanize_matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager, rc

# 폰트 설정
font_path = "fonts/malgun.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'

# 데이터 로드 및 전처리
@st.cache_data
def load_data(file_name):
    df = pd.read_csv(file_name, encoding="utf-8")
    df.columns = df.columns.str.strip()  # 열 이름 공백 제거
    return df

def preprocess_data(df, value_name):
    # 첫 두 행 제거 및 열 이름 정리
    df = df.iloc[1:].reset_index(drop=True)  # 첫 행 제거 후 인덱스 재설정
    
    # 필요한 열만 선택 ('구분'과 연도별 데이터)
    df = df.iloc[:, 3:]  # '구분' 열부터 시작하도록 조정
    
    # 데이터 변환 (긴 형식으로 변경)
    df = df.melt(id_vars=["구분"], var_name="연도", value_name=value_name)
    
    # 값에서 쉼표 제거 및 숫자로 변환 (등록 대수/판매 대수)
    if "대수" in value_name:
        df[value_name] = df[value_name].str.replace(",", "").astype(float)
    
    # 비중 데이터의 경우 % 기호 제거 후 숫자로 변환
    elif "비중" in value_name:
        df[value_name] = df[value_name].str.replace("%", "").astype(float)
    
    return df

# 데이터 로드 및 전처리
enroll_num = preprocess_data(load_data("enrollnum.csv"), "등록 대수")
enroll_per = preprocess_data(load_data("enrollper.csv"), "등록 비중")
sales_num = preprocess_data(load_data("salesnum.csv"), "판매 대수")
sales_per = preprocess_data(load_data("salesper.csv"), "판매 비중")

# Streamlit 애플리케이션
st.title("전기차 데이터 분석")
option = st.radio("데이터 유형 선택:", ["등록현황", "판매현황"])

if option == "등록현황":
    # 등록 대수 꺾은선 그래프
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for fuel in enroll_num['구분'].unique():
        fuel_data = enroll_num[enroll_num['구분'] == fuel]
        ax1.plot(fuel_data['연도'], fuel_data['등록 대수'], label=fuel)
    ax1.set_title("연료별 연도별 등록 대수")
    ax1.set_xlabel("연도")
    ax1.set_ylabel("등록 대수")
    ax1.legend()
    ax1.yaxis.set_major_locator(MultipleLocator(100000))

    # 등록 비중 원 그래프
    fig2, ax2 = plt.subplots()
    latest_year = enroll_per['연도'].max()
    latest_data = enroll_per[enroll_per['연도'] == latest_year]
    ax2.pie(latest_data['등록 비중'], 
            labels=latest_data['구분'], 
            autopct='%1.1f%%')
    ax2.set_title(f"{latest_year} 연료별 등록 비중")

    st.pyplot(fig1)
    st.pyplot(fig2)

elif option == "판매현황":
    # 판매 대수 꺾은선 그래프
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    for fuel in sales_num['구분'].unique():
        fuel_data = sales_num[sales_num['구분'] == fuel]
        ax3.plot(fuel_data['연도'], fuel_data['판매 대수'], label=fuel)
    ax3.set_title("연료별 연도별 판매 대수")
    ax3.set_xlabel("연도")
    ax3.set_ylabel("판매 대수")
    ax3.legend()
    ax3.yaxis.set_major_locator(MultipleLocator(100000))

    # 판매 비중 원 그래프
    fig4, ax4 = plt.subplots()
    latest_year = sales_per['연도'].max()
    latest_data = sales_per[sales_per['연도'] == latest_year]
    ax4.pie(latest_data['판매 비중'], 
            labels=latest_data['구분'], 
            autopct='%1.1f%%')
    ax4.set_title(f"{latest_year} 연료별 판매 비중")

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
    
    # 파일에 헤더 없이 추가 모드로 저장
    answer_df.to_csv("page1_answer.csv", mode='a', index=False, header=False)
    
    st.success("답변이 저장되었습니다.")
