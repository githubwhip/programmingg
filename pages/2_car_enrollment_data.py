import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import random
st.set_page_config(page_title="2_car_enrollment_data", layout="wide")  # 일반 모드 설정


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


import plotly.express as px

def plot_num_trend_interactive(data, vehicle_type):
    fig = px.line(
        data,
        x='연도',
        y='등록 대수',
        markers=True,
        title=f"{vehicle_type} 자동차는 연도별로 얼마나 등록됐을까"
    )
    fig.update_traces(mode="lines+markers", marker=dict(size=8), line=dict(width=3))
    
    # y축 숫자 형식 수정 (만 단위로 표시)
    fig.update_layout(
        xaxis_title="연도",
        yaxis_title="등록 대수",
        template="plotly_white",
        hovermode="x unified",
        height=500,  # 그래프 높이 통일
        margin=dict(l=40, r=40, t=60, b=40),  # 여백 설정
        yaxis=dict(tickformat=",.0f"),  # 천 단위로 콤마 추가
    )
    
    return fig


# Plotly로 버블 차트 생성
def plot_bubble_chart(data, vehicle_type):
    fig = px.scatter(
        data,
        x='연도',
        y='등록 비중',
        size='등록 비중',
        color='연도',
        title=f"{vehicle_type} 자동차는 연도별로 등록 비중이 어떻게 변화했을까",
        hover_name='연도',
        size_max=40,
        template='plotly_white',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        xaxis_title="연도",
        yaxis_title="등록 비중 (%)",
        height=500,  # 그래프 높이 통일
        margin=dict(l=40, r=40, t=60, b=40)  # 여백 설정
    )
    return fig

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        plot_num_trend_interactive(selected_num_data, selected_vehicle), 
        use_container_width=True, 
        key="plot_num_trend"
    )

with col2:
    st.plotly_chart(
        plot_bubble_chart(selected_per_data, selected_vehicle), 
        use_container_width=True, 
        key="plot_bubble"
    )

# "전기"를 선택했을 경우 버튼 추가
if selected_vehicle == "전기":
    # 세션 상태 초기화
    if "show_image" not in st.session_state:
        st.session_state.show_image = False  # 초기 상태는 숨김(False)

    # 세 개의 열 생성 (버튼을 오른쪽에 배치)
    col1, col2, col3 = st.columns([1, 1, 1])  # 비율 조정 가능

    # 오른쪽 열에 버튼 추가
    with col3:
        button = st.button("글로벌 전기차 침투율 살펴보기")

    # 버튼 클릭 시 상태를 토글
    if button:
        st.session_state.show_image = not st.session_state.show_image

    # 상태에 따라 이미지 표시 또는 숨기기
    if st.session_state.show_image:
        st.image("needle.png", caption="글로벌 전기차 침투율", use_container_width=True)


st.image("memo.png")
with st.container():
    answer_1 = st.text_input("✏️ 1. 학번과 이름을 적어주세요. (예: 2024-12345 홍길동)")
    
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
            st.balloons()
            st.download_button(
                label="📂 답변 엑셀 파일 다운로드",
                data=excel_data,
                file_name="answers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if st.button("📊 계속 학습하러 가기"):
    st.switch_page("pages/3_car_sales_data.py")
