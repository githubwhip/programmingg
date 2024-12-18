import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import koreanize_matplotlib
from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager, rc
from io import BytesIO

# 폰트 설정
font_path = "fonts/malgun.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'

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
enroll_num = preprocess_data(load_data("salesnum.csv"), "판매 대수")
enroll_per = preprocess_data(load_data("salesper.csv"), "판매 비중")

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
vehicle_types = enroll_num['구분'].dropna().unique().tolist()  # NaN 값 제거
vehicle_types = [x for x in vehicle_types if x != '소계']  # '소계' 제거
selected_vehicle = st.selectbox("차종을 선택하세요:", vehicle_types)

# 선택된 차종에 대한 데이터 필터링
selected_num_data = enroll_num[enroll_num['구분'] == selected_vehicle]
selected_per_data = enroll_per[enroll_per['구분'] == selected_vehicle]

# 두 개의 병렬 열 생성
col1, col2 = st.columns(2)

# 판매 대수 꺾은선 그래프 개선
with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_facecolor("#F9F9F9")  # 배경 색상
    ax1.plot(selected_num_data['연도'], selected_num_data['판매 대수'], 
             marker='o', color="#FF6F61", linestyle='-', linewidth=3, markersize=10, alpha=0.9)

    # 데이터 포인트 레이블
    for i, txt in enumerate(selected_num_data['판매 대수']):
        ax1.annotate(f'{int(txt):,}', 
                     (selected_num_data['연도'].iloc[i], txt), 
                     textcoords="offset points", xytext=(0, 10), 
                     ha='center', fontsize=12, color="blue", fontweight='bold')

    ax1.set_title(f"{selected_vehicle} 연도별 판매 대수", fontsize=20, color="#333333")
    ax1.set_xlabel("연도", fontsize=14, color="#555555")
    ax1.set_ylabel("판매 대수", fontsize=14, color="#555555")
    ax1.grid(axis="y", linestyle="--", alpha=0.5)  # 그리드 추가

    st.pyplot(fig1)

# 판매 비중 막대 그래프 개선
with col2:
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors = plt.cm.plasma_r(selected_per_data['판매 비중'] / selected_per_data['판매 비중'].max())

    bars = ax2.barh(selected_per_data['연도'], selected_per_data['판매 비중'], 
                    color=colors, edgecolor="black", alpha=0.9)
    
    # 막대 끝 숫자 강조
    for bar, value in zip(bars, selected_per_data['판매 비중']):
        ax2.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, 
                 f'{value:.1f}%', ha='left', va='center', fontsize=12, fontweight='bold', color="#333333")

    ax2.set_title(f"{selected_vehicle} 연도별 판매 비중", fontsize=20, color="#333333")
    ax2.set_xlabel("판매 비중 (%)", fontsize=14, color="#555555")
    ax2.set_ylabel("연도", fontsize=14, color="#555555")
    ax2.grid(axis="x", linestyle="--", alpha=0.5)  # 그리드 추가

    st.pyplot(fig2)

# 답변 입력 및 다운로드 섹션
st.image("memo.png")
answer_0 = st.text_input("✏️ 1. 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")

# 질문 섹션
def add_question(icon, title, question, input_type="text", image=None):
    with st.expander(f"{icon} {title}"):
        if image:
            st.image(image, use_container_width=True)
        if input_type == "text":
            return st.text_input(question)
        elif input_type == "textarea":
            return st.text_area(question)
        elif input_type == "select":
            return st.selectbox(question, ["선택하세요"] + ["100,000 단위", "50,000 단위", "1만 단위"])
        return None

answer_1 = add_question("⛽", "휘발유 판매 대수 및 비중 비교", 
                       "휘발유의 판매대수는 2020년도에 비해 2021년도가 낮습니다. 그러나 2020년도에 비해 2021년도의 휘발유의 등록 비중은 늘어났습니다. 그 이유를 추론해서 적어보세요.", image="alcohol.png")
answer_2 = add_question("📊", "LPG 차 꺾은선 그래프 눈금", 
                       "LPG 차 연도별 판매 대수 현황을 볼 때, 꺾은선 그래프의 눈금을 어떻게 표기하면 좋을까요?", image="lpg.png")
answer_3 = add_question("📈", "판매 대수와 비중 증가 차종", 
                       "시간이 흐름에 따라 판매 대수와 판매 비중이 증가하는 차종은 어떤 것인가요?", input_type="text")
answer_4 = add_question("📝", "판매 현황 조작 후 느낀 점", 
                       "여러분이 연도별 차종 판매 현황을 조작해보면서 느낀 점, 알게된 점, 궁금한 점 등을 자유롭게 서술해 주세요.", input_type="textarea")

# 답변 다운로드
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
        data_to_save = {"1. 학번": answer_0, "2. 휘발유 판매대수 및 비중": answer_1, 
                        "3. LPG 차 꺾은선 그래프": answer_2, "4. 판매 대수/비중 증가 차종": answer_3, 
                        "5. 느낀 점": answer_4}
        excel_data = download_answers(data_to_save)
        st.success("✅ 파일이 성공적으로 생성되었습니다!")
        st.balloons()
        st.download_button("📂 답변 엑셀 파일 다운로드", excel_data, "answers.xlsx")

if st.button("📊 계속 학습하러 가기"):
    st.switch_page("pages/ev car table.py")
