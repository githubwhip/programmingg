import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# 데이터 준비
data = {
    "구분": ["서울", "경기", "인천", "경북", "경남", "부산", "대구", "울산", "전북", "전남", 
            "광주", "충북", "충남", "대전", "세종", "강원", "제주", "전국"],
    "전기차(대)": [59327, 77648, 26242, 19154, 28120, 22063, 24161, 5061, 12727, 15387, 
                13249, 15140, 16611, 14673, 3034, 14012, 32976, 389855],
    "충전기(합계)": [34804, 50663, 9539, 9086, 11907, 11307, 11093, 3253, 6495, 8734, 
                6777, 6558, 7825, 7521, 2138, 4137, 5872, 194081]
}

df = pd.DataFrame(data)

# 지역 좌표 설정 (위도와 경도)
coordinates = {
    "서울": [37.5665, 126.9780],
    "경기": [37.4138, 127.5183],
    "인천": [37.4563, 126.7052],
    "경북": [36.5760, 128.5056],
    "경남": [35.4606, 128.2132],
    "부산": [35.1796, 129.0756],
    "대구": [35.8714, 128.6014],
    "울산": [35.5384, 129.3114],
    "전북": [35.7175, 127.1530],
    "전남": [34.8679, 126.9910],
    "광주": [35.1595, 126.8526],
    "충북": [36.6357, 127.4917],
    "충남": [36.6588, 126.6728],
    "대전": [36.3504, 127.3845],
    "세종": [36.4801, 127.2890],
    "강원": [37.8228, 128.1555],
    "제주": [33.4996, 126.5312],
}

# 지도 생성 함수
def create_map(column, title, color="blue"):
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df.iterrows():
        region = row["구분"]
        count = row[column]
        lat, lon = coordinates[region]
        folium.CircleMarker(
            location=[lat, lon],
            radius=count / 1000,  # 마커 크기 조정
            color=color,
            fill=True,
            fill_opacity=0.6,
            popup=f"{region}: {count:,}대"
        ).add_to(marker_cluster)

    return m

# Streamlit 앱 시작
st.title("전기차 및 충전기 현황 시각화")
st.write("탭을 선택해 전기차 및 충전기 현황을 확인하세요.")

# 탭 설정
tab1, tab2 = st.tabs(["전기차 현황", "충전기 현황"])

# 탭1: 전기차 지도 및 표
with tab1:
    st.subheader("전기차 등록 현황 지도")
    ev_map = create_map("전기차(대)", "전기차 등록 현황", color="blue")
    st_data = st_folium(ev_map, width=800, height=500)

    st.subheader("전기차 등록 현황 표")
    transposed_ev_df = df[["구분", "전기차(대)"]].set_index("구분").T  # 행과 열을 전환
    st.table(transposed_ev_df)

# 탭2: 충전기 지도 및 표
with tab2:
    st.subheader("충전기 설치 현황 지도")
    charger_map = create_map("충전기(합계)", "충전기 설치 현황", color="green")
    st_data = st_folium(charger_map, width=800, height=500)

    st.subheader("충전기 설치 현황 표")
    transposed_charger_df = df[["구분", "충전기(합계)"]].set_index("구분").T  # 행과 열을 전환
    st.table(transposed_charger_df)
