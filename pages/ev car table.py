import streamlit as st

# 웹페이지 레이아웃: 두 개의 열 생성
col1, col2 = st.columns(2)

# 왼쪽 열에 스크롤 가능한 표 표시
with col1:
    st.markdown(
        """
        <style>
        .scrollable-table {
            height: 400px; /* 원하는 높이 설정 */
            overflow-y: scroll;
            border: 1px solid #ddd;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            text-align: left;
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
        </style>
        <div class="scrollable-table">
        <table>
            <thead>
                <tr>
                    <th>지역</th>
                    <th>합계</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>서울</td><td>63,807</td></tr>
                <tr><td>경기</td><td>90,624</td></tr>
                <tr><td>인천</td><td>30,905</td></tr>
                <tr><td>경북</td><td>23,023</td></tr>
                <tr><td>경남</td><td>27,593</td></tr>
                <tr><td>부산</td><td>27,147</td></tr>
                <tr><td>대구</td><td>26,691</td></tr>
                <tr><td>울산</td><td>6,207</td></tr>
                <tr><td>전북</td><td>16,256</td></tr>
                <tr><td>전남</td><td>19,696</td></tr>
                <tr><td>광주</td><td>10,303</td></tr>
                <tr><td>충북</td><td>17,511</td></tr>
                <tr><td>충남</td><td>20,225</td></tr>
                <tr><td>대전</td><td>15,664</td></tr>
                <tr><td>세종</td><td>3,562</td></tr>
                <tr><td>강원</td><td>15,728</td></tr>
                <tr><td>제주</td><td>35,619</td></tr>
            </tbody>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 오른쪽 열에 지도 이미지 표시
with col2:
    st.image('map.png', caption="지역별 지도")


import streamlit as st
import pandas as pd
import folium
from folium import Marker
from streamlit_folium import st_folium

# 데이터 준비
regions = ["서울", "경기", "인천", "경북", "경남", "부산", "대구", "울산", "전북", "전남", "광주", "충북", "충남", "대전", "세종", "강원", "제주"]
종합 = [34602, 50663, 12939, 9608, 11097, 11307, 11093, 3253, 6495, 5734, 5677, 7825, 11201, 11476, 2206, 6437, 5872]

# 각 지역의 위도와 경도 (예시 좌표)
coordinates = {
    "서울": [37.5665, 126.9780],
    "경기": [37.4138, 127.5183],
    "인천": [37.4563, 126.7052],
    "경북": [36.5758, 128.5056],
    "경남": [35.4606, 128.2132],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "울산": [35.5384, 129.3114],
    "전북": [35.7175, 127.1530],
    "전남": [34.8161, 126.4630],
    "광주": [35.1595, 126.8526],
    "충북": [36.6357, 127.4913],
    "충남": [36.5184, 126.8000],
    "대전": [36.3504, 127.3845],
    "세종": [36.4800, 127.2890],
    "강원": [37.8228, 128.1555],
    "제주": [33.4996, 126.5312]
}

# DataFrame 생성
data = pd.DataFrame({"지역": regions, "종합": 종합})

# Folium 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 데이터 기반으로 마커 추가
for region in data.itertuples():
    name = region.지역
    total = region.종합
    coord = coordinates[name]
    
    folium.CircleMarker(
        location=coord,
        radius=total / 5000, # 종합 값에 비례한 크기 조정
        color="blue",
        fill=True,
        fill_color="blue",
        fill_opacity=0.6,
        tooltip=f"{name}: {total}"
    ).add_to(m)

# Streamlit에서 지도 표시
st.title("지역별 전기차 충전기 분포")
st_data = st_folium(m, width=700)
