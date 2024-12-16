import streamlit as st
import pandas as pd
import time



st.image('image.png')
data = pd.read_csv("members.csv")
data["PW"] = data["PW"].astype(str)

with st.form("login_form"):
    ID = st.text_input("ID", placeholder="아이디를 입력하세요")
    PW = st.text_input("Password", type="password", placeholder="비밀번호를 입력하세요")
    submit_button = st.form_submit_button("로그인")

if submit_button:
    if not ID or not PW:
        st.warning("ID와 비밀번호를 모두 입력해주세요.")
    else:
        # 사용자 확인
        class = data[(data["ID"] == ID) & (data["PW"] == str(PW))]
        
        if not user.empty:
            st.success(f"{ID}선생님의 반 학생 여러분, 환영합니다!")
            st.session_state["authenticated"]=True
            st.session_state["ID"] = ID
            
            progress_text = "접속 중입니다."
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            time.sleep(1)
            my_bar.empty()
        else:
            st.error("접속 정보가 일치하지 않습니다.")
