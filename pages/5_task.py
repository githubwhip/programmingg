import streamlit as st
import pandas as pd
from io import BytesIO

# 로그인 상태 확인
if not st.session_state.get("authenticated", False):
    st.warning("🔐 접속 확인이 필요합니다! [main 페이지로 돌아가서 선생님 성함과 비밀번호를 입력하고 다시 방문해 주세요.](./)")
    st.stop()

# 학번과 이름 입력 받기
answer_0 = st.text_input("👩‍🎓 1. 학번과 이름을 적어주세요. (예: 2024-25986 정유미)")

# 페이지 제목
st.header("🔋 충전기 통계 이미지 뷰어 📊")

# 탭 구성
tabs = ["⏰ 시간대별 충전 전력량", "📍 설치 장소별 이용 현황", "🍂 계절별 이용 현황"]
tab1, tab2, tab3 = st.tabs(tabs)

# 탭 1: 시간대별 충전 전력량 이미지와 질문
with tab1:
    st.image("충전기당시간대별평균충전전력량.png", use_container_width=True)
    with st.container():
        st.subheader("🔌 탭 1) 충전 속도별 이용 현황 분석")
        question_1 = st.selectbox(
            "1. 급속 충전기가 완속 충전기에 비해 높은 월평균 이용 횟수를 보이는 이유는 무엇인가요? 🤔",
            ["선택하세요", "짧은 충전 시간", "적은 운영 대수", "이동거점 위주 설치", "모두 해당"]
        )
        question_2 = st.selectbox(
            "2. 완속 충전기는 주로 어디에 설치되나요? 🏠",
            ["선택하세요", "고속도로 휴게소", "주택, 아파트 등의 생활거점", "지하철역 근처", "쇼핑몰 주차장"]
        )
        question_3 = st.selectbox(
            "3. 급속 충전기 중 어떤 종류가 가장 많이 설치되었나요? ⚡",
            ["선택하세요", "50kW", "100kW", "200kW", "350kW"]
        )
        question_4 = st.selectbox(
            "4. 200kW·350kW 급속 충전기의 주요 설치 위치는 어디인가요? 🛣️",
            ["선택하세요", "고속도로 휴게소", "대형 쇼핑몰", "도심지 공공시설", "주택가 근처"]
        )

# 탭 2: 설치 장소별 이용 현황 이미지와 질문
with tab2:
    st.image("충전기당설치장소별월평균이용현황.png", use_container_width=True)
    with st.container():
        st.subheader("🏝️ 탭 2) 설치 장소별 이용 현황 분석")
        question_1 = st.selectbox(
            "1. 월평균 이용 횟수가 가장 높은 지역은 어디인가요? 🌍",
            ["선택하세요", "서울", "제주", "부산", "경기도"]
        )
        question_2 = st.selectbox(
            "2. 제주 지역의 월평균 이용 횟수가 높은 이유는 무엇인가요? 🌞",
            ["선택하세요", "급속 충전기 비중이 높기 때문", "저렴한 전기 요금", "인구 밀도가 낮기 때문", "기후 조건이 적합"]
        )
        question_3 = st.selectbox(
            "3. 부산의 월평균 이용 횟수가 낮은 이유는 무엇일까요? 🚶",
            ["선택하세요", "급속 충전기 비중이 낮기 때문", "인구 밀도가 너무 높다", "전기차 보급률이 낮기 때문", "모든 답이 해당"]
        )
        question_4 = st.selectbox(
            "4. 급속 충전기가 많은 지역은 어느 곳일까요? 🚗",
            ["선택하세요", "서울", "제주", "부산", "경기도"]
        )

# 탭 3: 계절별 이용 현황 이미지와 질문
with tab3:
    st.image("충전기당계절별월평균이용현황.png", use_container_width=True)
    with st.container():
        st.subheader("🍃 탭 3) 계절별 이용 현황 분석")
        question_1 = st.selectbox(
            "1. 사계절 중 월평균 이용 횟수가 가장 많은 계절은 무엇인가요? 🌸",
            ["선택하세요", "여름", "가을", "겨울", "봄"]
        )
        question_2 = st.selectbox(
            "2. 겨울철 충전기 이용 시간이 더 긴 이유는 무엇인가요? ❄️",
            ["선택하세요", "전기차 배터리 성능 저하", "추운 날씨로 충전기 효율이 낮아짐", "이용자들이 급속 충전기를 많이 사용하기 때문", "기타 이유"]
        )
        question_3 = st.selectbox(
            "3. 급속 충전기 이용 횟수가 가장 많은 계절은 무엇인가요? 🌞",
            ["선택하세요", "여름", "가을", "겨울", "봄"]
        )
        question_4 = st.selectbox(
            "4. 봄철 충전기 이용 횟수가 적은 이유는 무엇일까요? 🌱",
            ["선택하세요", "낮은 전기차 보급률", "날씨가 따뜻하여 충전 필요성이 적음", "사용자들이 급속 충전기를 피함", "기타 이유"]
        )

# 답변을 모아 엑셀 파일로 저장 및 다운로드
def download_answers(answers):
    df = pd.DataFrame(list(answers.items()), columns=["질문", "답변"])
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Answers")
    return output.getvalue()

if st.button("💾 답변 파일 생성하기"):
    if not answer_0:
        st.warning("⚠️ 학번과 이름을 입력하세요!")
    else:
        data_to_save = {
            "1. 학번": answer_0,
            "2. 충전 속도별 이용 현황": {
                "급속 충전기가 완속 충전기에 비해 높은 월평균 이용 횟수를 보이는 이유": question_1,
                "완속 충전기의 주 설치 장소": question_2,
                "급속 충전기 중 설치된 가장 많은 종류": question_3,
                "200kW·350kW 급속 충전기의 주요 설치 위치": question_4,
            },
            "3. 설치 장소별 이용 현황": {
                "월평균 이용 횟수가 가장 높은 지역": question_1,
                "제주 지역의 높은 월평균 이용 횟수 이유": question_2,
                "부산의 낮은 월평균 이용 횟수 이유": question_3,
                "급속 충전기가 많은 지역": question_4,
            },
            "4. 계절별 이용 현황": {
                "사계절 중 월평균 이용 횟수가 가장 많은 계절": question_1,
                "겨울철 충전기 이용 시간이 긴 이유": question_2,
                "급속 충전기 이용 횟수가 가장 많은 계절": question_3,
                "봄철 충전기 이용 횟수가 적은 이유": question_4,
            }
        }
        
        excel_data = download_answers(data_to_save)
        st.success("✅ 파일이 성공적으로 생성되었습니다! 🎉")
        st.balloons()  # 폭죽 효과 출력
        st.download_button(
            label="📥 답변 엑셀 파일 다운로드",
            data=excel_data,
            file_name="answers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
