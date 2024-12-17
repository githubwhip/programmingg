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
    st.subheader("🔌 탭 1) 시간대별 충전 전력량 분석")
    question_1 = st.selectbox(
        "1. 급속 충전이 주로 많이 사용되는 시간대는 언제인가요? ⏰",
        ["선택하세요", "오전 (6-12시)", "오후 (12-18시)", "저녁 (18-24시)", "새벽 (0-6시)"]
    )
    question_2 = st.selectbox(
        "2. 완속 충전이 주로 사용되는 시간대는 언제인가요? 🌙",
        ["선택하세요", "오전 (6-12시)", "오후 (12-18시)", "저녁 (18-24시)", "새벽 (0-6시)"]
    )

# 탭 2: 설치 장소별 이용 현황 이미지와 질문
with tab2:
    st.image("충전기당설치장소별월평균이용현황.png", use_container_width=True)
    st.subheader("🏝️ 탭 2) 설치 장소별 이용 현황 분석")
    question_3 = st.selectbox(
        "1. 어느 장소에서 완속 충전기가 가장 많이 사용되나요? 🏠",
        ["선택하세요", "주거지역", "상업시설", "휴게소", "기타시설"]
    )
    question_4 = st.selectbox(
        "2. 급속 충전기는 주로 어떤 장소에 설치되나요? 🚗",
        ["선택하세요", "고속도로 휴게소", "상업시설", "주차시설", "교육문화시설"]
    )

# 탭 3: 계절별 이용 현황 이미지와 질문
with tab3:
    st.image("충전기당계절별월평균이용현황.png", use_container_width=True)
    st.subheader("🍃 탭 3) 계절별 이용 현황 분석")
    question_5 = st.selectbox(
        "1. 급속 충전기가 가장 많이 이용되는 계절은 언제인가요? 🌞",
        ["선택하세요", "봄", "여름", "가을", "겨울"]
    )
    question_6 = st.selectbox(
        "2. 겨울철 충전 시간은 다른 계절보다 긴 이유는 무엇인가요? ❄️",
        ["선택하세요", "배터리 성능 저하", "날씨가 추워 충전 효율이 낮아짐", "사용량 증가", "기타 이유"]
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
            "2. 시간대별 이용 현황": {
                "급속 충전이 많이 사용되는 시간대": question_1,
                "완속 충전이 많이 사용되는 시간대": question_2,
            },
            "3. 설치 장소별 이용 현황": {
                "완속 충전기가 가장 많이 사용되는 장소": question_3,
                "급속 충전기가 설치된 장소": question_4,
            },
            "4. 계절별 이용 현황": {
                "급속 충전기가 많이 사용되는 계절": question_5,
                "겨울철 충전 시간이 긴 이유": question_6,
            }
        }
        
        excel_data = download_answers(data_to_save)
        st.success("✅ 파일이 성공적으로 생성되었습니다! 🎉")
        st.balloons()
        st.download_button(
            label="📥 답변 엑셀 파일 다운로드",
            data=excel_data,
            file_name="answers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
