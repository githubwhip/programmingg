import streamlit as st
import pandas as pd
import time



st.image('image.png')
data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)

with st.form("login_form"):
    ID = st.text_input("ID", placeholder="선생님 성함을 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("학생 접속")

if submit_button:
    if not ID or not PW:
        st.warning("선생님 성함과 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인
        class = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
# 로그인 성공 시
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

ID = "정유미"  # 예제 ID
st.success(f"{ID}선생님의 반 학생 여러분, 환영합니다!")
st.session_state["authenticated"] = True
st.session_state["ID"] = ID

# 진행 상태 표시
progress_text = "접속 중입니다."
progress_bar = st.progress(0)
status = st.empty()

for percent_complete in range(100):
    time.sleep(0.01)  # 진행률 조절
    progress_bar.progress(percent_complete + 1)
    status.text(f"{percent_complete + 1}% 완료")

# 진행 완료 후 UI 초기화
time.sleep(1)
progress_bar.empty()
status.empty()

st.success("접속이 완료되었습니다!")
