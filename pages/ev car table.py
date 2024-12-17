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
