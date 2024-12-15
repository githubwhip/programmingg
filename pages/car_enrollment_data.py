import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import koreanize_matplotlib
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
enroll_num = preprocess_data(load_data("enrollnum.csv"), "등록 대수")
enroll_per = preprocess_data(load_data("enrollper.csv"), "등록 비중")

# 그래프 생성 함수
def plot_num_trend(data, vehicle_type):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['연도'], data['등록 대수'], marker='o')
    ax.set_title(f"{vehicle_type} 연도별 등록 대수")
    ax.set_xlabel("연도")
    ax.set_ylabel("등록 대수")
    ax.set_yticklabels([])

    for i, txt in enumerate(data['등록 대수']):
        ax.annotate(f'{int(txt):,}', (data['연도'].iloc[i], txt), textcoords="offset points", xytext=(0, 10), ha='center')

    return fig

def plot_percentage_trend(data, vehicle_type):
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(len(data))]
    ax.barh(data['연도'], data['등록 비중'], color=colors)
    ax.set_title(f"{vehicle_type} 연도별 등록 비중")
    ax.set_xlabel("등록 비중 (%)")
    ax.set_ylabel("연도")

    for i, v in enumerate(data['등록 비중']):
        ax.text(v, i, f'{v:.1f}%', va='center', ha='left')

    return fig

# Streamlit 애플리케이션 시작
st.title("차종별 연도별 등록 현황")

# 사용자 입력: 차종 선택
vehicle_types = enroll_num['구분'].unique()
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]
selected_per_data = enroll_per[enroll_per['구분'] == selected_vehicle]

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)
with col1:
    st.pyplot(plot_num_trend(selected_num_data, selected_vehicle))
with col2:
    st.pyplot(plot_percentage_trend(selected_per_data, selected_vehicle))

# 학습지 섹션
st.header("학습지")

# 학습지 질문
def add_question(image, question):
    st.image(image, width=300)
    return st.text_input(question)

answer_1 = add_question("hybrid.png", 
                        "1. 하이브리드 차 연도별 등록 대수 현황을 볼 때, 꺾은선 그래프의 눈금을 어떻게 표기하면 좋을까요? (예: 100,000부터 시작하여 10만 단위 간격으로 표시 등)")
answer_2 = add_question("oil.png", 
                        "2. 경유의 등록대수는 2019년도에 비해 2020년도가 높습니다. 그러나 2019년도에 비해 2020년도의 경유의 등록 비중은 줄어들었다. 그 이유를 추론해서 적어보세요.")
answer_3 = st.text_input("3. 시간이 흐름에 따라 등록 대수와 등록 비중이 증가하는 차종은 어떤 것인가요? (예: 휘발유 등)")
answer_4 = st.text_area("4. 여러분이 연도별 차종 등록 현황을 조작해보면서 느낀 점, 알게된 점, 궁금한 점 등을 자유롭게 서술해 주세요.")

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
        "1. 하이브리드 차 관련 질문": answer_1,
        "2. 경유 관련 질문": answer_2,
        "3. 등록 대수/비중 증가 차종": answer_3,
        "4. 느낀 점": answer_4,
        "로그인 정보": {
            "username": st.session_state.get('username', '로그인 정보 없음')
        }
    }
    excel_data = download_answers(data_to_save)
    st.download_button(label="답변 엑셀 파일 다운로드",
                       data=excel_data,
                       file_name="answers.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
