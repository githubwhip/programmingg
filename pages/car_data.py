import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib import font_manager, rc

# 폰트 설정
font_path = "fonts/malgun.ttf"
font_manager.fontManager.addfont(font_path)
rc('font', family='Malgun Gothic')
plt.rcParams['font.family'] = 'Malgun Gothic'

# 데이터 로드 및 전처리 함수
@st.cache_data
def load_and_preprocess(file_name, value_name):
    df = pd.read_csv(file_name, encoding="utf-8")
    df.columns = df.columns.str.strip()
    df = df.iloc[1:].reset_index(drop=True)  # 첫 행 제거 후 인덱스 재설정
    df.columns = ["구분"] + list(df.columns[1:])  # 첫 번째 열은 '구분', 나머지는 연도로 설정
    df = df.melt(id_vars=["구분"], var_name="연도", value_name=value_name)  # 긴 형식으로 변환
    
    # 값 정리 (쉼표 제거 및 숫자로 변환)
    if "대수" in value_name:
        df[value_name] = df[value_name].str.replace(",", "").astype(float)
    elif "비중" in value_name:
        df[value_name] = df[value_name].str.replace("%", "").astype(float)
    
    return df

# 데이터 로드
enroll_num = load_and_preprocess("enrollnum.csv", "등록 대수")
sales_num = load_and_preprocess("salesnum.csv", "판매 대수")

# Streamlit 애플리케이션
st.title("차종별 등록 및 판매 현황 분석")

# 첫 번째 선택: 등록현황 또는 판매현황
option = st.radio("데이터 유형 선택:", ["등록현황", "판매현황"])

# 두 번째 선택: 차종 선택
if option == "등록현황":
    fuel_type = st.selectbox("차종을 선택하세요:", enroll_num["구분"].unique())
    selected_data = enroll_num[enroll_num["구분"] == fuel_type]
else:
    fuel_type = st.selectbox("차종을 선택하세요:", sales_num["구분"].unique())
    selected_data = sales_num[sales_num["구분"] == fuel_type]

# 선택한 데이터 시각화
if not selected_data.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(selected_data["연도"], selected_data[selected_data.columns[-1]], marker="o", label=fuel_type)
    ax.set_title(f"{fuel_type}의 연도별 {option}")
    ax.set_xlabel("연도")
    ax.set_ylabel(f"{option} 대수")
    ax.legend()
    ax.yaxis.set_major_locator(MultipleLocator(100000))  # Y축 눈금 설정
    
    st.pyplot(fig)
else:
    st.write("선택한 차종에 대한 데이터가 없습니다.")
