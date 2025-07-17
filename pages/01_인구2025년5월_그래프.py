import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("2025년 5월 기준 연령별 인구 현황 및 지도 시각화")

# CSV 파일 읽기 (파일명과 경로는 환경에 맞게 수정)
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 숫자 변환
df['총인구수'] = pd.to_numeric(df['2025년05월_계_총인구수'].str.replace(',', ''), errors='coerce').fillna(0).astype(int)

# 연령별 컬럼 추출 및 컬럼명 변경
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 인구수 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 행정구역별 위도/경도 (직접 작성, JSON 등 사용 안 함)
location_dict = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '인천광역시': [37.4563, 126.7052],
    '경기도': [37.4138, 127.5183],
    '대구광역시': [35.8714, 128.6014],
}

# top5_df에서 좌표가 있는 행정구역만 필터링
top5_df = top5_df[top5_df['행정구역'].isin(location_dict.keys())]

# 지도 생성 (서울 기준)
m = folium.Map(location=[37.5665, 126.9780], zoom_start=7)

# 원형 반투명 마커 추가
for idx, row in top5_df.iterrows():
    loc = location_dict[row['행정구역']]
    popup_text = f"{row['행정구역']}<br>총인구수: {row['총인구수']:,}"
    folium.CircleMarker(
        location=loc,
        radius=20,
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.4,
        popup=popup_text,
        tooltip=row['행정구역']
    ).add_to(m)

# Streamlit에서 folium 지도 출력
st.subheader("🏙️ 상위 5개 행정구역 지도 표시")
st_folium(m, width=700, height=500)
