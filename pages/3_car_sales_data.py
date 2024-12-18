import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import koreanize_matplotlib

# Streamlit 앱 설정
st.set_page_config(page_title="차종별 판매 현황", layout="wide")
st.title("🚗 차종별 연도별 판매 현황 대시보드")

# 로그인 확인
if not st.session_state.get("authenticated", False):
    st.warning("접속 확인이 필요합니다. [main 페이지로 돌아가서 성함과 비밀번호를 입력하고 다시 방문해 주세요.](./)")
    st.stop()

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_preprocess_data(num_file, per_file):
    # 판매 대수 데이터 로드
    df_num = pd.read_csv(num_file, encoding="utf-8")
    df_num = df_num[~df_num['구분'].isin(['합계', '기타', '소계'])].reset_index(drop=True)
    df_num = df_num.melt(id_vars=["구분"], var_name="연도", value_name="판매 대수")
    df_num['판매 대수'] = df_num['판매 대수'].str.replace(",", "").astype(int)
    
    # 판매 비중 데이터 로드
    df_per = pd.read_csv(per_file, encoding="utf-8")
    df_per = df_per[~df_per['구분'].isin(['합계', '기타', '소계'])].reset_index(drop=True)
    df_per = df_per.melt(id_vars=["구분"], var_name="연도", value_name="판매 비중")
    df_per['판매 비중'] = df_per['판매 비중'].str.replace("%", "").astype(float)
    
    return df_num, df_per

# 데이터 불러오기
sales_num, sales_per = load_and_preprocess_data("salesnum.csv", "salesper.csv")

# 사용자 입력: 차종 선택
vehicle_types = sales_num['구분'].unique().tolist()
selected_vehicle = st.selectbox("🔍 차종을 선택하세요:", vehicle_types)

# 선택된 차종 데이터 필터링
filtered_num = sales_num[sales_num['구분'] == selected_vehicle]
filtered_per = sales_per[sales_per['구분'] == selected_vehicle]

# 2개의 열로 나눠 인터랙티브 그래프 표시
col1, col2 = st.columns(2)

# 판매 대수 Plotly 꺾은선 그래프
with col1:
    st.subheader("📈 연도별 판매 대수 변화")
    fig_num = px.line(
        filtered_num, 
        x="연도", 
        y="판매 대수", 
        title=f"{selected_vehicle} 연도별 판매 대수",
        markers=True,
        template="plotly_white"
    )
    fig_num.update_traces(line=dict(width=3), marker=dict(size=10, color="red"))
    st.plotly_chart(fig_num, use_container_width=True)

# 판매 비중 Plotly 막대그래프
with col2:
    st.subheader("📊 연도별 판매 비중 비교")
    fig_per = px.bar(
        filtered_per, 
        x="판매 비중", 
        y="연도", 
        title=f"{selected_vehicle} 연도별 판매 비중",
        text="판매 비중",
        orientation="h",
        template="plotly_white",
        color="판매 비중",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig_per.update_traces(texttemplate='%{text:.2f}%', textposition="outside")
    st.plotly_chart(fig_per, use_container_width=True)

# 사용자 질문 및 답변 섹션
st.subheader("📝 학습 질문")
answer_0 = st.text_input("1️⃣ 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")

st.write("2️⃣ 질문에 대한 답변을 작성해 보세요.")
answer_1 = st.text_area("휘발유 판매대수와 비중에 대한 분석을 작성해 주세요.")
answer_2 = st.text_area("LPG 차 꺾은선 그래프 눈금을 어떻게 표기하면 좋을까요?")
answer_3 = st.text_area("판매 대수와 비중이 증가하는 차종을 적어보세요.")
answer_4 = st.text_area("데이터를 조작하며 느낀 점과 알게 된 점을 자유롭게 적어주세요.")

# 답변 파일 다운로드
def download_answers(answers):
    df = pd.DataFrame(list(answers.items()), columns=["질문", "답변"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Answers")
    return output.getvalue()

if st.button("📝 답변 파일 생성하기"):
    if not answer_0:
        st.warning("⚠️ 학번과 이름을 입력하세요!")
    else:
        answers = {
            "학번과 이름": answer_0,
            "휘발유 판매대수 분석": answer_1,
            "LPG 그래프 눈금": answer_2,
            "증가하는 차종": answer_3,
            "느낀 점": answer_4
        }
        excel_data = download_answers(answers)
        st.success("✅ 답변 파일이 생성되었습니다!")
        st.download_button("📂 답변 파일 다운로드", excel_data, "answers.xlsx")

if st.button("🔄 계속 학습하기"):
    st.switch_page("pages/ev car table.py")
