import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# 데이터프레임 생성
df = pd.DataFrame({
    '지역': ['서울', '경기', '인천', '강원', '충북', '충남', '대전', '세종', '경북', '경남', '부산', '대구', '울산', '전북', '전남', '광주', '제주'],
    '위도': [37.5665, 37.4138, 37.4563, 37.8228, 36.6357, 36.6588, 36.3504, 36.4800, 36.0190, 35.2383, 35.1796, 35.8714, 35.5384, 35.8242, 34.8161, 35.1595, 33.4890],
    '경도': [126.9780, 127.5183, 126.7052, 128.1555, 127.4914, 126.6728, 127.3845, 127.2890, 129.3434, 128.6919, 129.0756, 128.6014, 129.3114, 127.1480, 126.4631, 126.8526, 126.4983],
    '합계': [63807, 90624, 30905, 15728, 17511, 20225, 15564, 3562, 23023, 27147, 27551, 26691, 6207, 16256, 19966, 10303, 35619]
})

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 마커 클러스터 생성
marker_cluster = MarkerCluster().add_to(m)

# 원형 마커와 텍스트 추가
for idx, row in df.iterrows():
    folium.Circle(
        location=[row['위도'], row['경도']],
        radius=row['합계']/100,  # 원의 크기 조절
        popup=f"{row['지역']}: {row['합계']}",
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.4
    ).add_to(marker_cluster)
    
    folium.map.Marker(
        [row['위도'], row['경도']],
        icon=folium.DivIcon(html=f"<div style='font-size: 10pt; font-weight: bold;'>{row['지역']}<br>{row['합계']:,}</div>")
    ).add_to(marker_cluster)

# 스트림릿에 지도 표시
st.title('지역별 자동차 등록 현황')
folium_static(m)
