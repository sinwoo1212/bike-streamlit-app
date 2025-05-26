import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import altair as alt

st.set_page_config(layout="wide")
st.title("서울시 공공자전거 대여소 현황 시각화")

# 샘플 데이터 직접 생성
data = {
    '대여소명': ['강남역', '서울역', '여의도', '홍대입구', '건대입구'],
    '구': ['강남구', '중구', '영등포구', '마포구', '광진구'],
    '위도': [37.4979, 37.5547, 37.5269, 37.5563, 37.5409],
    '경도': [127.0276, 126.9707, 126.9249, 126.9237, 127.0705],
    '보유대수': [30, 25, 20, 22, 18]
}
df = pd.DataFrame(data)

# 사이드바 필터
districts = df['구'].unique()
district = st.sidebar.selectbox("구 선택", ["전체"] + list(districts))
search_name = st.sidebar.text_input("대여소명 검색")

filtered = df
if district != "전체":
    filtered = filtered[filtered['구'] == district]
if search_name:
    filtered = filtered[filtered['대여소명'].str.contains(search_name)]

# 지도
m = folium.Map(location=[37.55, 126.98], zoom_start=11)
for _, row in filtered.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=f"{row['대여소명']} (자전거 수: {row['보유대수']})",
        icon=folium.Icon(color='blue', icon='bicycle', prefix='fa')
    ).add_to(m)

st.subheader("서울시 공공자전거 대여소 위치")
st_data = st_folium(m, width=700, height=500)

# 차트
st.subheader("대여소별 보유 자전거 수")
bar_chart = alt.Chart(filtered).mark_bar().encode(
    x=alt.X('대여소명', sort='-y', title='대여소명'),
    y=alt.Y('보유대수', title='보유 자전거 수'),
    tooltip=['대여소명', '보유대수']
).properties(width=700, height=300)

st.altair_chart(bar_chart)
