import streamlit as st
import pandas as pd
import time

FONT_PATH = "fonts/malgun.ttf"
FONT_CSS = f"""
<style>
    @font-face {{
        font-family: 'Malgun Gothic';
        src: url('{FONT_PATH}');
    }}
    html, body, [class*="st-"] {{
        font-family: 'Malgun Gothic', sans-serif;
    }}
</style>
"""
st.markdown(FONT_CSS, unsafe_allow_html=True)
# 이미지 출력
st.image('image.png')

# 데이터 불러오기
data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)  # 비밀번호를 문자열로 변환

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# 로그인 폼
with st.form("login_form"):
    ID = st.text_input("ID", placeholder="선생님 성함을 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("학생 접속")

# 로그인 검증
if submit_button:
    if not ID or not PW:
        st.warning("선생님 성함과 비밀번호를 모두 입력해주세요.")
    else:
        # ID와 PW 일치 여부 확인
        user_data = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user_data.empty:  # 로그인 성공
            st.session_state["authenticated"] = True
            st.session_state["ID"] = ID

            # 진행 상태 표시
            st.success(f"{ID} 선생님의 반 학생 여러분, 환영합니다!")
            progress_text = "접속 중입니다."
            progress_bar = st.progress(0)
            status = st.empty()

            for percent_complete in range(100):
                time.sleep(0.01)  # 진행률 조절
                progress_bar.progress(percent_complete + 1)
                status.text(f"{percent_complete + 1}% 완료")

            time.sleep(1)  # 진행 완료 후 대기
            progress_bar.empty()
            status.empty()
            st.success("접속이 완료되었습니다!")
        else:
            st.error("접속 정보가 일치하지 않습니다.")
