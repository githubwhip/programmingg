import streamlit as st
import pandas as pd

# Initialize session state for user ID
if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

# Sidebar showing user ID
with st.sidebar:
    st.caption(f'{ID}님 접속중')

# Load pedestrian light data from CSV with appropriate encoding (likely CP949 for Korean)
try:
    data = pd.read_csv("보행등위도경도.csv", encoding='cp949')  # Use 'euc-kr' if cp949 doesn't work
except UnicodeDecodeError:
    st.error("파일을 읽는 중에 오류가 발생했습니다. 인코딩을 확인해주세요.")
    st.stop()

# Title of the app
st.title('서울 지역 보행등 위치 현황')

# Fill any missing values with 0 (if necessary)
data = data.copy().fillna(0)

# Example of creating a size column based on some relevant field (adjust as needed)
data['size'] = 10  # Set a fixed size for all points, or adjust based on your data

# Define colors for all districts (자치구) in Seoul
color_map = {
    '강남구': '#37eb91',
    '서초구': '#ebbb37',
    '송파구': '#eb3737',
    '종로구': '#37a2eb',
    '강동구': '#a237eb',
    '강북구': '#ff5733',
    '강서구': '#33ff57',
    '관악구': '#5733ff',
    '광진구': '#ff33a2',
    '구로구': '#a2ff33',
    '금천구': '#33a2ff',
    '노원구': '#ffa233',
    '도봉구': '#33ffa2',
    '동대문구': '#a233ff',
    '동작구': '#ff5733',
    '마포구': '#57ff33',
    '서대문구': '#3357ff',
    '성동구': '#ff33a2',
    '성북구': '#a2ff57',
    '양천구': '#33a2ff',
    '영등포구': '#ffa233',
    '용산구': '#33ffa2',
    '은평구': '#a233ff',
    '종로구': '#ff5733',
    '중구': '#57ff33',
    '중랑구': '#3357ff'
}

# Create a color column based on 자치구
data['color'] = data['자치구'].map(color_map).fillna('#cccccc')  # Default color if not mapped

# Show a map with locations marked by latitude and longitude, sized by 'size', and colored by 'color'
st.map(data, latitude="위도", longitude="경도", size="size", color="color")