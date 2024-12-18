import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import random

# 로그인 상태 확인
if not st.session_state.get("authenticated", False):
    st.warning("접속 확인이 필요합니다. [main 페이지로 돌아가서 선생님 성함과 비밀번호를 입력하고 다시 방문해 주세요.](./)")
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

# Streamlit 애플리케이션 시작
st.image("car.png")
st.markdown(
    """
    <h4 style="margin-top: 40px; margin-bottom: 20px;">🚗 <b>차종을 골라볼까요?</b> 🚗✨</h4>
    <p>여러분이 궁금한 차종을 골라 <b>연도별 등록 대수</b>를 한눈에 확인해 보세요! 🧐</p>
    <p>오른쪽 차트에서는 <i>차종의 연도별 등록 비중</i>도 함께 볼 수 있어요! 🔍</p>
    <p><b>어느 차종이 가장 인기가 많을까요?</b> 🎯</p>
    <p style="margin-bottom: 45px;">그럼 시작해볼까요? 🍀🚗</p>
    """,
    unsafe_allow_html=True
)

# 사용자 입력: 차종 선택
vehicle_types = enroll_num['구분'].unique()
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]
selected_per_data = enroll_per[enroll_per['구분'] == selected_vehicle]

# Plotly로 인터랙티브 꺾은선 그래프 생성
def plot_num_trend_interactive(data, vehicle_type):
    fig = px.line(data, x='연도', y='등록 대수', markers=True, title=f"{vehicle_type} 연도별 등록 대수")
    fig.update_traces(mode="lines+markers", marker=dict(size=8), line=dict(width=3))
    fig.update_layout(
        xaxis_title="연도",
        yaxis_title="등록 대수",
        template="plotly_white",
        hovermode="x unified"
    )
    return fig
# Plotly로 버블 차트 생성
def plot_bubble_chart(data, vehicle_type):
    fig = px.scatter(
        data,
        x='연도',  # x축: 연도
        y='등록 비중',  # y축: 등록 비중
        size='등록 비중',  # 버블 크기: 등록 비중에 따라 설정
        color='연도',  # 연도별 색상
        title=f"{vehicle_type} 연도별 등록 비중 버블 차트",
        hover_name='연도',  # 마우스를 올렸을 때 표시될 항목
        size_max=40,  # 버블의 최대 크기 설정
        template='plotly_white',
        color_continuous_scale='Viridis'  # 색상 팔레트
    )
    fig.update_layout(
        xaxis_title="연도",
        yaxis_title="등록 비중 (%)",
        font=dict(size=12),
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(plot_num_trend_interactive(selected_num_data, selected_vehicle), use_container_width=True)

with col2:
    st.plotly_chart(plot_bubble_chart(selected_per_data, selected_vehicle), use_container_width=True)


# 추가 질문 및 답변 저장 (기존 코드 그대로 사용)
st.image("memo.png")
with st.container():
    answer_1 = st.text_input("✏️ 1. 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")
    
    def add_question(icon, title, question, input_type="text", image=None):
        with st.expander(f"{icon} {title}"):
            if image:
                st.image(image, use_container_width=True)
            if input_type == "text":
                return st.text_input(question)
            elif input_type == "textarea":
                return st.text_area(question)
            elif input_type == "select":
                return st.selectbox(question, ["선택하세요", "50만 단위", "10만 단위", "5만 단위", "1만 단위"])
        return None

    # 각 질문 추가
    answer_2 = add_question("🚘", "하이브리드 차 꺾은선 그래프 눈금", "눈금을 어떻게 표기할까요?", "select", "hybrid.png")
    answer_3 = add_question("⛽", "경유 등록 대수 및 비중 비교", "경유 등록 비중 감소 이유를 추론하세요.", "textarea", "oil.png")
    answer_4 = add_question("📈", "등록 대수와 비중 증가 차종", "어떤 차종이 증가했나요?")
    answer_5 = add_question("🚀", "연도별 현황 조작 후 느낀 점", "느낀 점을 자유롭게 서술하세요.", "textarea")

    # 답변 저장 및 다운로드
    def download_answers(answers):
        df = pd.DataFrame(list(answers.items()), columns=["질문", "답변"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Answers")
        return output.getvalue()

    if st.button("📝 답변 파일 생성하기"):
        if not answer_1:
            st.warning("⚠️ 학번과 이름을 입력하세요!")
        else:
            data_to_save = {
                "1. 학번": answer_1,
                "2. 하이브리드 차 관련 질문": answer_2,
                "3. 경유 관련 질문": answer_3,
                "4. 등록 대수/비중 증가 차종": answer_4,
                "5. 느낀 점": answer_5
            }

            excel_data = download_answers(data_to_save)
            st.success("✅ 파일이 성공적으로 생성되었습니다!")
            st.download_button(
                label="📂 답변 엑셀 파일 다운로드",
                data=excel_data,
                file_name="answers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if st.button("📊 계속 학습하러 가기"):
    st.switch_page("pages/car_sales_data.py")
