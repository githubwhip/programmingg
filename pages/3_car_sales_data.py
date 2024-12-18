import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
from io import BytesIO
import time

st.set_page_config(page_title="3_car_sales_data", layout="wide")  # Wide 모드 설정

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
st.image("car2.png")

st.markdown(
    """
    <div style="margin: 50px 0;">
        <h4>🚗 차종별 연도별 판매 현황을 살펴보세요!</h4>
        <p>좌측 그래프에서 <strong>판매 대수의 변화</strong>를 확인하고,</p>
        <p>우측 그래프에서는 각 연도별 <strong>판매 비중</strong>을 비교해 보세요! 🎯</p>
        <p>판매 트렌드를 파악하면 어떤 차종이 인기인지 알 수 있을 거예요! 📊✨</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 사용자 입력: 차종 선택
vehicle_types = enroll_num['구분'].dropna().unique().tolist()
vehicle_types = [x for x in vehicle_types if x != '소계']
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종에 대한 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]
selected_per_data = enroll_per[enroll_per['구분'] == selected_vehicle]

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)

import plotly.graph_objects as go
import streamlit as st

# "판매 대수"를 "만" 단위로 변환
selected_num_data['판매 대수(만)'] = selected_num_data['판매 대수'] / 10000

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=selected_num_data['연도'],
        y=selected_num_data['판매 대수(만)'],
        mode='lines+markers+text',
        text=[f"{int(x):,}" for x in selected_num_data['판매 대수(만)']],
        textposition='top center',
        marker=dict(size=10, color='blue'),
        line=dict(width=3, color='blue')
    ))
    fig1.update_layout(
        title=f"{selected_vehicle} 연도별 판매 대수",
        xaxis_title="연도",
        yaxis_title="판매 대수 (만 단위)",
        font=dict(size=14),
        height=500,  # 그래프 높이 통일
        margin=dict(l=40, r=40, t=60, b=40),  # 마진 통일
    )
    st.plotly_chart(fig1, use_container_width=True)


# 버블 차트 (판매 비중)
with col2:
    fig2 = px.scatter(
        selected_per_data,
        x='연도',  # x축: 연도
        y='판매 비중',  # y축: 판매 비중
        size='판매 비중',  # 버블 크기: 판매 비중에 따라 크기를 설정
        color='연도',  # 색상: 연도별로 색상을 다르게 설정
        title=f"{selected_vehicle} 연도별 판매 비중 버블 차트",
        color_continuous_scale='Viridis',  # 색상 팔레트 설정
        hover_name='연도',  # 마우스를 올렸을 때 표시할 항목
        size_max=40,  # 버블의 최대 크기 설정 (조정 가능)
        template='plotly',  # 기본 템플릿 설정 (스타일)
    )
    fig2.update_layout(
        xaxis_title="연도",
        yaxis_title="판매 비중 (%)",
        font=dict(size=14),
        height=500,  # 그래프 높이 통일
        margin=dict(l=40, r=40, t=60, b=40),  # 마진 통일
    )
    st.plotly_chart(fig2, use_container_width=True)



import streamlit as st
import pandas as pd
from io import BytesIO

# 페이지 헤더

st.image("memo.png")

# 학번과 이름 입력
answer_0 = st.text_input("✏️ 1. 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")

# 질문 섹션 함수
def add_question(icon, title, question, input_type="text", image=None):
    """
    Add a question with optional icon, image, and input type within an expander.
    """
    with st.expander(f"{icon} {title}"):
        if image:
            st.image(image, use_container_width=True)  # 최신 버전 대응
        if input_type == "text":
            return st.text_input(question)
        elif input_type == "textarea":
            return st.text_area(question)
        elif input_type == "select":
            return st.selectbox(question, ["선택하세요"] + ["100,000 단위", "50,000 단위", "1만 단위"])
        return None

# 질문 1: 휘발유 판매대수
answer_1 = add_question(
    icon="⛽",
    title="휘발유 판매 대수 및 비중 비교",
    question="휘발유의 판매대수는 2020년도에 비해 2021년도가 낮습니다. 그러나 2020년도에 비해 2021년도의 휘발유의 등록 비중은 늘어났습니다. 그 이유를 추론해서 적어보세요.",
    image="alcohol.png"
)

# 질문 2: LPG 차 꺾은선 그래프
answer_2 = add_question(
    icon="📊",
    title="LPG 차 꺾은선 그래프 눈금",
    question="LPG 차 연도별 판매 대수 현황을 볼 때, 꺾은선 그래프의 눈금을 어떻게 표기하면 좋을까요? \n(예: 100,000부터 시작하여 1만 단위 간격으로 표시 등)",
    image="lpg.png"
)

# 질문 3: 증가하는 차종
answer_3 = add_question(
    icon="📈",
    title="판매 대수와 비중 증가 차종",
    question="시간이 흐름에 따라 판매 대수와 판매 비중이 증가하는 차종은 어떤 것인가요? \n(예: 휘발유 등)",
    input_type="text"
)

# 질문 4: 자유 서술
answer_4 = add_question(
    icon="📝",
    title="판매 현황 조작 후 느낀 점",
    question="여러분이 연도별 차종 판매 현황을 조작해보면서 느낀 점, 알게된 점, 궁금한 점 등을 자유롭게 서술해 주세요.",
    input_type="textarea"
)

# 답변을 모아 엑셀 파일로 저장 및 다운로드
def download_answers(answers):
    df = pd.DataFrame(list(answers.items()), columns=["질문", "답변"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Answers")
    return output.getvalue()

# 파일 생성 및 다운로드 버튼
if st.button("📝 답변 파일 생성하기"):
    if not answer_0:
        st.warning("⚠️ 학번과 이름을 입력하세요!")
    else:
        data_to_save = {
            "1. 학번": answer_0,
            "2. 휘발유 판매대수 및 비중": answer_1,
            "3. LPG 차 꺾은선 그래프": answer_2,
            "4. 판매 대수/비중 증가 차종": answer_3,
            "5. 느낀 점": answer_4
        }
        
        excel_data = download_answers(data_to_save)
        st.success("✅ 파일이 성공적으로 생성되었습니다!")
        st.balloons()  # 폭죽 효과 출력
        st.download_button(
            label="📂 답변 엑셀 파일 다운로드",
            data=excel_data,
            file_name="answers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if st.button("📊 계속 학습하러 가기"):
    st.switch_page("pages/ev car table.py")
