import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import koreanize_matplotlib
from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager, rc
from io import BytesIO
import time

# 폰트 설정
font_path = "fonts/malgun.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'


#로그인 상태 확인
if not st.session_state.get("authenticated", False):
    st.warning("로그인이 필요합니다. [로그인 페이지로 돌아가기](./)")
    st.stop()



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
enroll_num = preprocess_data(load_data("salesnum.csv"), "판매 대수")
enroll_per = preprocess_data(load_data("salesper.csv"), "판매 비중")  # 등록 비중 데이터 추가

# Streamlit 애플리케이션 시작
st.title("차종별 연도별 판매 현황")

# 사용자 입력: 차종 선택
# 사용자 입력: 차종 선택
vehicle_types = enroll_num['구분'].dropna().unique().tolist()  # NaN 값 제거
vehicle_types = [x for x in vehicle_types if x != '소계']  # '소계' 제거
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종에 대한 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]
selected_per_data = enroll_per[enroll_per['구분'] == selected_vehicle]

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)


with col1:
    # 등록 대수 꺾은선 그래프 생성
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    # 폰트 크기 설정
    plt.rcParams['font.size'] = 14  # 기본 폰트 크기
    ax1.tick_params(axis='both', labelsize=12)  # 축 레이블 크기
    ax1.set_title(f"{selected_vehicle} 연도별 판매 대수", fontsize=20)  # 제목 크기
    ax1.set_xlabel("연도", fontsize=14)  # x축 레이블 크기
    ax1.set_ylabel("판매 대수", fontsize=14)  # y축 레이블 크기
    
    # 데이터 포인트 레이블 크기 증가
    for i, txt in enumerate(selected_num_data['판매 대수']):
        ax1.annotate(f'{int(txt):,}', (selected_num_data['연도'].iloc[i], txt), 
                    textcoords="offset points", xytext=(0, 10), 
                    ha='center', fontsize=12)
  
    # 그래프 그리기
    ax1.plot(selected_num_data['연도'], selected_num_data['판매 대수'], marker='o')
    ax1.set_title(f"{selected_vehicle} 연도별 판매 대수")
    ax1.set_xlabel("연도")
    ax1.set_ylabel("판매 대수")
    
    # 세로축 숫자 레이블 제거
    ax1.set_yticklabels([])

    # 그래프 출력
    st.pyplot(fig1)
    
with col2:
    # 등록 비중 막대 그래프 생성 (가로 방향)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(selected_per_data))]
        
    # 폰트 크기 설정
    ax2.tick_params(axis='both', labelsize=12)  # 축 레이블 크기
    ax2.set_title(f"{selected_vehicle} 연도별 판매 비중", fontsize=20)  # 제목 크기
    ax2.set_xlabel("판매 비중 (%)", fontsize=14)  # x축 레이블 크기
    ax2.set_ylabel("연도", fontsize=14)  # y축 레이블 크기
    
    # 퍼센트 레이블 크기 증가
    for i, v in enumerate(selected_per_data['판매 비중']):
        ax2.text(v, i, f'{v:.1f}%', va='center', ha='left', fontsize=12)



    # '판매 비중' 열을 사용하도록 수정
    ax2.barh(selected_per_data['연도'], selected_per_data['판매 비중'], color=colors)
    ax2.set_title(f"{selected_vehicle} 연도별 판매 비중")
    ax2.set_xlabel("판매 비중 (%)")
    ax2.set_ylabel("연도")


    # 그래프 출력
    st.pyplot(fig2)

# 학습지 섹션 추가
st.header("학습지")

# 학번과 이름을 입력 받는 부분
answer_0 = st.text_input("1. 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")

# 질문 1
st.image("alcohol.png")
answer_1 = st.text_input("1. 휘발유의 판매대수는 2020년도에 비해 2021년도가 낮습니다. 그러나 2020년도에 비해 2021년도의 휘발유의 등록 비중은 늘어났습니다. \n그 이유를 추론해서 적어보세요.")

# 질문 2
st.image("lpg.png")
answer_2 = st.text_input("2. LPG 차 연도별 판매 대수 현황을 볼 때, 꺾은선 그래프의 눈금을 어떻게 표기하면 좋을까요? \n(예: 100,000부터 시작하여 1만 단위 간격으로 표시 등)")

# 질문 3
answer_3 = st.text_input("3. 시간이 흐름에 따라 판매 대수와 판매 비중이 증가하는 차종은 어떤 것인가요? \n(예: 휘발유 등)")

# 질문 4
answer_4 = st.text_area("4. 여러분이 연도별 차종 판매 현황을 조작해보면서 느낀 점, 알게된 점, 궁금한 점 등을 자유롭게 서술해 주세요.")

# 답변을 모아 엑셀 파일로 저장 및 다운로드
def download_answers(answers):
    df = pd.DataFrame(list(answers.items()), columns=["질문", "답변"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Answers")
    return output.getvalue()

import json

if st.button("답변 파일 다운로드"):
    data_to_save = {
        "1. 학번": answer_0,
        "1. 휘발유 판매대수": answer_1,
        "2. LPG 차 판매 대수": answer_2,
        "3. 판매 대수/비중 증가 차종": answer_3,
        "4. 느낀 점": answer_4
    }
    
    excel_data = download_answers(data_to_save)
    st.download_button(label="답변 엑셀 파일 다운로드",
                       data=excel_data,
                       file_name="answers.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if st.button("계속 학습하러 가기"):
    st.switch_page("pages/car_sales_data.py")
