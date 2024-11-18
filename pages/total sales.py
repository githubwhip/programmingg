import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from matplotlib import font_manager, rc
from matplotlib.ticker import FuncFormatter
import os
import matplotlib.font_manager as font_manager

# 폰트 파일의 경로 설정
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'malgun.ttf')
font_name = font_manager.FontProperties(fname=font_path).get_name()

# matplotlib에 폰트 설정
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = font_name


# CSV 파일 불러오기 (인코딩 문제 해결을 위해 cp949 사용)
file_path = '매출현황.csv'
data = pd.read_csv(file_path, encoding='cp949')

# 해외교포의 마지막 행 제외
data = data[data['구분'] != '해외교포'].iloc[:-1]

# 월별 데이터 추출 함수
def get_monthly_data(df, nationality, period, metric):
    # 선택한 기간에 따라 해당 월 필터링
    if period == "1~4월":
        months = ['1월', '2월', '3월', '4월']
    elif period == "5~8월":
        months = ['5월', '6월', '7월', '8월']
    else:
        months = ['9월', '10월', '11월', '12월']
    
    # 선택한 국적의 데이터 필터링
    filtered_data = df[df['구분'] == nationality]
    
    # 선택한 지표에 따라 이용객수 또는 매출액 데이터 선택
    if metric == "이용객수":
        monthly_data = filtered_data[[f'{month} 이용객' for month in months]].values.flatten()
    else:
        monthly_data = filtered_data[[f'{month} 순매출액' for month in months]].values.flatten()
    
    return months, monthly_data

# y축 포맷터 함수 (값에 따라 적절한 단위로 표시)
def format_func(x, _):
    if x >= 1_000_000:
        return f'{int(x / 1_000_000)}백만'
    elif x >= 1_000:
        return f'{int(x / 1_000)}천'
    else:
        return f'{int(x)}'

# Streamlit UI 구성
st.title("매출 현황 분석")

# 1. 국적 선택
nationality = st.selectbox("국적을 선택하세요", data['구분'].unique())

# 2. 기간 선택
period = st.selectbox("기간을 선택하세요", ["1~4월", "5~8월", "9~12월"])

# 3. 이용객수 또는 매출액 선택
metric = st.radio("이용객수 또는 매출액을 선택하세요", ["이용객수", "순매출액"])

# 4. 조회 버튼
if st.button("조회"):
    # 데이터 추출
    months, values = get_monthly_data(data, nationality, period, metric)
    
    # 그래프 색상 랜덤 설정
    color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    
    # 그래프 그리기 (꺾은선 그래프)
    plt.figure(figsize=(10, 6))
    plt.plot(months, values, marker='o', color=color, linestyle='-', linewidth=2)
    
    # y축 간격 및 포맷 설정 (단위에 맞게 표시)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
    
    # 그래프 제목 및 레이블 설정
    plt.title(f"{nationality}의 {period} {metric} 현황")
    plt.xlabel("월")
    plt.ylabel(metric)
    
    # 범례 추가
    plt.legend([f"{nationality} {metric}"])
    
    # 그래프 출력
    st.pyplot(plt)
