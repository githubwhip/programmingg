import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Initialize session state for user ID
if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

# Sidebar showing user ID
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# Load CSV data
try:
    data = pd.read_csv("page1.csv", encoding='cp949')  # Use 'euc-kr' if cp949 doesn't work
except UnicodeDecodeError:
    st.error("파일을 읽는 중에 오류가 발생했습니다. 인코딩을 확인해주세요.")
    st.stop()

# Title of the app
st.title('전기차 데이터를 파헤쳐보자!')

# Menu for selection
menu = st.radio("데이터를 선택하세요:", ["등록현황", "판매현황"])

# Helper function for random colors
def random_color(count=1):
    return [f"#{''.join(random.choices('0123456789ABCDEF', k=6))}" for _ in range(count)]

# Plotting graphs
if menu == "등록현황":
    st.subheader("등록현황 데이터 시각화")
    # Filter and prepare data for 등록현황
    registration_data = data.groupby(['연도', '연료', '구분'])['등록대수'].sum().reset_index()

    # Separate 국내 and 수입
    domestic_data = registration_data[registration_data['구분'] == '국내']
    import_data = registration_data[registration_data['구분'] == '수입']

    # Plot graphs
    fig, ax = plt.subplots(2, 2, figsize=(14, 12))

    # 국내 등록현황 꺾은선그래프
    for fuel in domestic_data['연료'].unique():
        fuel_data = domestic_data[domestic_data['연료'] == fuel]
        ax[0, 0].plot(fuel_data['연도'], fuel_data['등록대수'], label=fuel, color=random_color()[0])
    ax[0, 0].set_title("국내 - 연도별 연료별 등록대수")
    ax[0, 0].set_xlabel("연도")
    ax[0, 0].set_ylabel("등록대수")
    ax[0, 0].legend()

    # 수입 등록현황 꺾은선그래프
    for fuel in import_data['연료'].unique():
        fuel_data = import_data[import_data['연료'] == fuel]
        ax[0, 1].plot(fuel_data['연도'], fuel_data['등록대수'], label=fuel, color=random_color()[0])
    ax[0, 1].set_title("수입 - 연도별 연료별 등록대수")
    ax[0, 1].set_xlabel("연도")
    ax[0, 1].set_ylabel("등록대수")
    ax[0, 1].legend()

    # Pie charts for the latest year
    latest_year = max(data['연도'])
    domestic_latest = domestic_data[domestic_data['연도'] == latest_year]
    import_latest = import_data[import_data['연도'] == latest_year]

    ax[1, 0].pie(domestic_latest['등록대수'], labels=domestic_latest['연료'], autopct='%1.1f%%', colors=random_color(len(domestic_latest)))
    ax[1, 0].set_title(f"국내 - {latest_year} 연료별 등록 비중")
    ax[1, 1].pie(import_latest['등록대수'], labels=import_latest['연료'], autopct='%1.1f%%', colors=random_color(len(import_latest)))
    ax[1, 1].set_title(f"수입 - {latest_year} 연료별 등록 비중")

    st.pyplot(fig)

elif menu == "판매현황":
    st.subheader("판매현황 데이터 시각화")
    # Filter and prepare data for 판매현황
    sales_data = data.groupby(['연도', '연료', '구분'])['판매대수'].sum().reset_index()

    # Separate 국내 and 수입
    domestic_sales = sales_data[sales_data['구분'] == '국내']
    import_sales = sales_data[sales_data['구분'] == '수입']

    # Plot graphs
    fig, ax = plt.subplots(2, 2, figsize=(14, 12))

    # 국내 판매현황 꺾은선그래프
    for fuel in domestic_sales['연료'].unique():
        fuel_data = domestic_sales[domestic_sales['연료'] == fuel]
        ax[0, 0].plot(fuel_data['연도'], fuel_data['판매대수'], label=fuel, color=random_color()[0])
    ax[0, 0].set_title("국내 - 연도별 연료별 판매대수")
    ax[0, 0].set_xlabel("연도")
    ax[0, 0].set_ylabel("판매대수")
    ax[0, 0].legend()

    # 수입 판매현황 꺾은선그래프
    for fuel in import_sales['연료'].unique():
        fuel_data = import_sales[import_sales['연료'] == fuel]
        ax[0, 1].plot(fuel_data['연도'], fuel_data['판매대수'], label=fuel, color=random_color()[0])
    ax[0, 1].set_title("수입 - 연도별 연료별 판매대수")
    ax[0, 1].set_xlabel("연도")
    ax[0, 1].set_ylabel("판매대수")
    ax[0, 1].legend()

    # Pie charts for the latest year
    domestic_latest = domestic_sales[domestic_sales['연도'] == latest_year]
    import_latest = import_sales[import_sales['연도'] == latest_year]

    ax[1, 0].pie(domestic_latest['판매대수'], labels=domestic_latest['연료'], autopct='%1.1f%%', colors=random_color(len(domestic_latest)))
    ax[1, 0].set_title(f"국내 - {latest_year} 연료별 판매 비중")
    ax[1, 1].pie(import_latest['판매대수'], labels=import_latest['연료'], autopct='%1.1f%%', colors=random_color(len(import_latest)))
    ax[1, 1].set_title(f"수입 - {latest_year} 연료별 판매 비중")

    st.pyplot(fig)

# Display a question section below the graphs
st.subheader("질문에 답변해 보세요!")
question1 = st.text_input("(1) 연도별 전기차의 등록현황과 판매현황은 어떠한가요?")
question2 = st.text_input("(2) 왜 그런 현상이 나타났을까요? 본인의 생각을 자유롭게 서술해 보세요.")

# Save answers to CSV
if st.button("답변 제출"):
    try:
        # Prepare the new data
        answer_data = pd.DataFrame([{
            "ID": ID,
            "P1A1": question1,
            "P1A2": question2
        }])
        
        # Append to the file or create a new one
        try:
            existing_data = pd.read_csv("page1_answer.csv", encoding="cp949")
            answer_data = pd.concat([existing_data, answer_data], ignore_index=True)
        except FileNotFoundError:
            pass  # No existing file, create a new one

        # Save the data
        answer_data.to_csv("page1_answer.csv", index=False, encoding="cp949")
        st.success("답변이 저장되었습니다!")
    except Exception as e:
        st.error(f"답변 저장 중 오류가 발생했습니다: {e}")
