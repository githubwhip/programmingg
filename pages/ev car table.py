import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 기존 데이터 준비
data = {
    "구분": ["서울", "경기", "인천", "경북", "경남", "부산", "대구", "울산", "전북", "전남", 
            "광주", "충북", "충남", "대전", "세종", "강원", "제주", "전국"],
    "전기차(대)": [59327, 77648, 26242, 19154, 28120, 22063, 24161, 5061, 12727, 15387, 
                13249, 15140, 16611, 14673, 3034, 14012, 32976, 389855],
    "충전기(합계)": [34804, 50663, 9539, 9086, 11907, 11307, 11093, 3253, 6495, 8734, 
                6777, 6558, 7825, 7521, 2138, 4137, 5872, 194081]
}

df = pd.DataFrame(data)

# 이미지 데이터 준비 (새로운 표)
data_image = {
    "구분": ["서울", "경기", "인천", "경북", "경남", "부산", "대구", "울산",
            "전북", "전남", "광주", "충북", "충남", "대전", "세종", "강원", "제주", "전국"],
    "충전기(종합)": [34602, 50663, 9539, 9608, 11097, 11307, 11093, 3253, 
                   6495, 5734, 5677, 6558, 7825, 5721, 2600, 6437, 5872, 194081],
    "급속": [2255, 3701, 867, 1781, 1359, 652, 999, 494,
            1070, 1162, 510, 905, 1101, 593, 218, 1176, 1798, 20641],
    "완속": [32437, 46962, 8672, 7827, 9738, 10655, 10094, 2759,
            5425, 4572, 5167, 5653, 6724, 5128, 2382, 5261, 4074, 173440]
}

df_image = pd.DataFrame(data_image)

# 지역 좌표 설정
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
    "전국": [36.5, 127.5]
}

# 지도 생성 함수
def create_map1(column, color="blue"):
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    for idx, row in df.iterrows():
        region = row["구분"]
        if region == "전국":  # 전국 데이터 제외
            continue

        count = row[column]
        lat, lon = coordinates.get(region, (None, None))
        if lat and lon:
            folium.CircleMarker(
                location=[lat, lon],
                radius=count / 2500,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=f"{region}: {count:,}대"
            ).add_to(m)

    return m

def create_map(column, color="blue"):
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    for idx, row in df.iterrows():
        region = row["구분"]
        if region == "전국":  # 전국 데이터 제외
            continue

        count = row[column]
        lat, lon = coordinates.get(region, (None, None))
        if lat and lon:
            folium.CircleMarker(
                location=[lat, lon],
                radius=count / 2500,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=f"{region}: {count:,}대"
            ).add_to(m)

    return m

def create_map2(column, color="blue"):
    m = folium.Map(location=[36.5, 127.5], zoom_start=7)

    for idx, row in df.iterrows():
        region = row["구분"]
        if region == "전국":  # 전국 데이터 제외
            continue

        count = row[column]
        lat, lon = coordinates.get(region, (None, None))
        if lat and lon:
            folium.CircleMarker(
                location=[lat, lon],
                radius=count / 2000,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=f"{region}: {count:,}대"
            ).add_to(m)

    return m


# Streamlit 레이아웃
st.title("지역별 전기차 등록 현황 및 충전기 설치 현황 알아보기")

# 페이지 나누기
left_col, right_col = st.columns([2, 1])

# 왼쪽 부분 (탭 2개로 지도 표시)
with left_col:
    tab1, tab2 = st.tabs(["전기차", "충전기"])

    with tab1:
        ev_map = create_map1("전기차(대)", color="blue")
        st_folium(ev_map, width=700, height=500)

    with tab2:
        charger_map = create_map2("충전기(합계)", color="green")
        st_folium(charger_map, width=700, height=500)

# 오른쪽 부분 (탭 2개로 테이블 표시)
with right_col:
    table_tab1, table_tab2 = st.tabs(["전기차/충전기", "급속/완속 충전기"])

    with table_tab1:
        st.dataframe(df.set_index("구분"), use_container_width=True)

    with table_tab2:
        st.dataframe(df_image.set_index("구분"), use_container_width=True)
