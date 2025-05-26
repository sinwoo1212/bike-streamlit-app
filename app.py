import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import altair as alt

st.set_page_config(layout="wide")
st.title("서울시 공공자전거 대여소 현황 시각화")

# 1. 데이터 불러오기 (서울시 공공자전거 대여소 API 또는 CSV)
@st.cache_data
def load_data():
    url = "https://data.seoul.go.kr/dataList/OA-15493/S/1/datasetView.do"  
    # 서울시 공공자전거 대여소 공식 API가 복잡하니 여기선 미리 저장된 csv로 가정
    # 실제 배포시엔 직접 CSV를 GitHub에 올리고 불러오는 방식을 추천
    csv_url = "https://raw.githubusercontent.com/sinwoo1212/sample-data/main/seoul_bike_stations.csv"
    df = pd.read_csv(csv_url)
    return df

df = load_data()

# 2. 사이드바 필터
districts = df['구'].unique()
district = st.sidebar.selectbox("구 선택", ["전체"] + list(districts))
search_name = st.sidebar.text_input("대여소명 검색")

if district != "전체":
    df = df[df['구'] == district]
if search_name:
    df = df[df['대여소명'].str.contains(search_name)]

# 3. 지도 생성
m = folium.Map(location=[37.55, 126.98], zoom_start=11)
for _, row in df.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=f"{row['대여소명']} (자전거 수: {row['보유대수']})",
        icon=folium.Icon(color='blue', icon='bicycle', prefix='fa')
    ).add_to(m)

st.subheader("서울시 공공자전거 대여소 위치")
st_data = st_folium(m, width=700, height=500)

# 4. 대여소별 자전거 보유 수 차트
st.subheader("대여소별 보유 자전거 수")
bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X('대여소명', sort='-y', title='대여소명'),
    y=alt.Y('보유대수', title='보유 자전거 수'),
    tooltip=['대여소명', '보유대수']
).properties(width=700, height=300)

st.altair_chart(bar_chart)

# 5. 방문일과 메모 (간단하게 local state 사용)
st.sidebar.subheader("방문 계획 및 메모")
visit_date = st.sidebar.date_input("방문 날짜")
memo = st.sidebar.text_area("메모 입력")

if st.sidebar.button("저장"):
    st.sidebar.success(f"{visit_date}에 방문 계획이 저장되었습니다.")
    # 실제 저장은 서버 없이는 불가능하니 간단히 확인 메시지 출력

