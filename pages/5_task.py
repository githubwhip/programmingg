import streamlit as st

# 로그인 상태 확인
if not st.session_state.get("authenticated", False):
    st.warning("🔐 접속 확인이 필요합니다! [main 페이지로 돌아가서 선생님 성함과 비밀번호를 입력하고 다시 방문해 주세요.](./)")
    st.stop()

# 정답 설정
correct_answers = {
    "급속 시간대": "오후 (12-18시)",
    "완속 시간대": "저녁 (18-24시)",
    "완속 설치 장소": "공공시설",
    "급속 설치 장소": "주차시설",
    "급속 계절": "가을",
    "겨울 충전 이유": "배터리 성능 저하"
}

# 페이지 제목
st.image("car4.png")
st.markdown(
    """
    <h4 style="margin-top: 20px; margin-bottom: 10px;">🔋 <b>전기차 충전기 사용 실태를 분석해볼까요?</b> 🚗✨</h4>
    <p>여러분은 <b>전기차 충전</b>에 대해 얼마나 알고 있나요? 🧐</p>
    <p>지금부터 <i>시간대별 충전 전력량</i>, <i>설치 장소별 이용 현황</i>, 그리고 <i>계절별 이용 현황</i>에 대한 문제를 풀어보세요! 📊</p>
    <p><b>총 6개의 문제가 준비되어 있어요!</b> 🔍</p>
    <p style="margin-top: 15px;">그럼 시작해볼까요? <b>행운을 빌어요!</b> 🍀🚗</p>
    """,
    unsafe_allow_html=True
)


# 탭 구성
tabs = ["⏰ 시간대별 충전 전력량", "📍 설치 장소별 이용 현황", "🍂 계절별 이용 현황"]
tab1, tab2, tab3 = st.tabs(tabs)

# 사용자 입력 변수 초기화
answers = {}

# 탭 1: 시간대별 충전 전력량
with tab1:
    st.image("충전기당시간대별평균충전전력량.png", use_container_width=True)
    st.subheader("🔌 시간대별 충전 전력량 분석")
    answers["급속 충전 시간대"] = st.selectbox(
        "1. 급속 충전이 주로 많이 사용되는 시간대는 언제인가요? ⏰",
        ["선택하세요", "오전 (6-12시)", "오후 (12-18시)", "저녁 (18-24시)", "새벽 (0-6시)"]
    )
    answers["완속 충전 시간대"] = st.selectbox(
        "2. 완속 충전 사용량이 증가하는 시간대는 언제인가요? 🌙",
        ["선택하세요", "오전 (6-12시)", "오후 (12-18시)", "저녁 (18-24시)", "새벽 (0-6시)"]
    )

# 탭 2: 설치 장소별 이용 현황
with tab2:
    st.image("충전기당설치장소별월평균이용현황.png", use_container_width=True)
    st.subheader("🏝️ 설치 장소별 이용 현황 분석")
    answers["완속 충전기 설치 장소"] = st.selectbox(
        "3. 어느 장소에서 완속 충전기가 가장 많이 사용되나요? 🏠",
        ["선택하세요", "공공시설", "차량정비시설", "휴게소", "기타시설"]
    )
    answers["급속 충전기 설치 장소"] = st.selectbox(
        "4. 급속 충전기는 주로 어떤 장소에 설치되나요? 🚗",
        ["선택하세요", "고속도로 휴게소", "상업시설", "주차시설", "공공주택시"]
    )

# 탭 3: 계절별 이용 현황
with tab3:
    st.image("충전기당계절별월평균이용현황.png", use_container_width=True)
    st.subheader("🍃 계절별 이용 현황 분석")
    answers["급속 충전기 사용 계절"] = st.selectbox(
        "5. 급속 충전기가 가장 많이 이용되는 계절은 언제인가요? 🌞",
        ["선택하세요", "봄", "여름", "가을", "겨울"]
    )
    answers["겨울철 충전시간이 긴 이유"] = st.selectbox(
        "6. 겨울철 충전 시간이 더 긴 이유는 무엇인가요? ❄️",
        ["선택하세요", "배터리 성능 저하", "날씨가 추워 충전 효율이 높아짐", "사용량 감", "기타 이유"]
    )

# 채점 기능
if st.button("📋 제출하기"):
    if not answer_0:
        st.warning("⚠️ 학번과 이름을 입력하세요!")
    else:
        incorrect = []
        for key, value in correct_answers.items():
            if answers.get(key) != value:
                incorrect.append(key)

        if not incorrect:  # 모두 맞았을 경우
            st.success("🎉 축하합니다! 모든 문제를 맞혔습니다! 🎉")
            st.balloons()
        else:  # 틀린 문제가 있을 경우
            st.warning("😢 아쉽게도 틀린 문제가 있어요. 다시 시도해보세요!")
            for question in incorrect:
                st.write(f"❗ **{question}** 다시 생각해보세요.")
