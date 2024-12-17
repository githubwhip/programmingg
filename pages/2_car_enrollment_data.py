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
st.image("car.png")

st.markdown(
    """
    
    **🔍 차종을 선택해보세요!**  
    궁금한 연도별 등록 대수를 살펴볼 수 있어요.  
    오른쪽 차트에서는 **등록 비중**도 확인할 수 있답니다! 🎯  

    
    """
)

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

import streamlit as st
import pandas as pd
from io import BytesIO

import streamlit as st
import pandas as pd
from io import BytesIO

import streamlit as st
import pandas as pd
from io import BytesIO

import streamlit as st
import pandas as pd
from io import BytesIO

# 페이지 헤더
st.header("🚗 학습지 작성하기")

# 전체 컨테이너 시작 (스크롤 지원)
with st.container():
    # 학번과 이름 입력
    answer_1 = st.text_input("✏️ 1. 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")

    # 질문 입력 함수
    def add_question(icon, title, question, input_type="text", image=None):
        """
        Add a question with optional icon, image, and input type within an expander.
        """
        with st.expander(f"{icon} {title}"):
            if image:
                st.image(image, use_container_width=True)  # Updated parameter
            if input_type == "text":
                return st.text_input(question)
            elif input_type == "textarea":
                return st.text_area(question)
            elif input_type == "select":
                return st.selectbox(question, ["선택하세요"] + ["50만 단위", "10만 단위", "5만 단위", "1만 단위"])
            elif input_type == "slider":
                return st.slider(question, min_value=0, max_value=10, step=1)
        return None

    # 질문 2: 하이브리드 차 관련
    answer_2 = add_question(
        icon="🚘", 
        title="하이브리드 차 꺾은선 그래프 눈금",
        question="하이브리드 차 연도별 등록 대수 현황을 볼 때, 꺾은선 그래프의 눈금을 어떻게 표기하면 좋을까요?",
        input_type="select",
        image="hybrid.png"
    )

    # 질문 3: 경유 관련 질문
    answer_3 = add_question(
        icon="⛽", 
        title="경유 등록 대수 및 비중 비교",
        question="경유의 등록대수는 2019년도에 비해 2020년도가 높습니다. 그러나 2019년도에 비해 2020년도의 경유의 등록 비중은 줄어들었다. 그 이유를 추론해서 적어보세요.",
        input_type="textarea",
        image="oil.png"
    )

    # 질문 4: 등록 대수/비중 증가 차종
    answer_4 = add_question(
        icon="📈", 
        title="등록 대수와 비중이 증가한 차종",
        question="시간이 흐름에 따라 등록 대수와 등록 비중이 증가하는 차종은 어떤 것인가요? (예: 휘발유 등)",
        input_type="text"
    )

    # 질문 5: 자유 서술
    answer_5 = add_question(
        icon="🚀", 
        title="연도별 현황 조작 후 느낀 점",
        question="여러분이 연도별 차종 등록 현황을 조작해보면서 느낀 점, 알게된 점, 궁금한 점 등을 자유롭게 서술해 주세요.",
        input_type="textarea"
    )

    # 답변을 엑셀 파일로 저장
    def download_answers(answers):
        df = pd.DataFrame(list(answers.items()), columns=["질문", "답변"])
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Answers")
        return output.getvalue()

    # 파일 생성 및 다운로드 버튼
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
            st.balloons()  # 폭죽 효과 출력
            st.download_button(
                label="📂 답변 엑셀 파일 다운로드",
                data=excel_data,
                file_name="answers.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if st.button("📊 계속 학습하러 가기"):
    st.switch_page("pages/car_sales_data.py")
