import streamlit as st

# 페이지 제목
st.title("🔋 충전기 통계 이미지 뷰어")

# 탭 구성
tabs = ["시간대별 충전 전력량", "설치 장소별 이용 현황", "계절별 이용 현황"]
tab1, tab2, tab3 = st.tabs(tabs)

# 탭 1: 시간대별 충전 전력량 이미지
with tab1:
    st.header("⏰ 충전기당 시간대별 평균 충전 전력량")
    st.image("충전기당시간대별평균충전전력량.png", use_container_width=True)

# 탭 2: 설치 장소별 이용 현황 이미지
with tab2:
    st.header("🏢 충전기당 설치 장소별 월평균 이용 현황")
    st.image("충전기당설치장소별월평균이용현황.png", use_container_width=True)

# 탭 3: 계절별 이용 현황 이미지
with tab3:
    st.header("🌤️ 충전기당 계절별 월평균 이용 현황")
    st.image("충전기당계절별월평균이용현황.png", use_container_width=True)
