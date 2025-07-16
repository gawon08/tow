import streamlit as st
import pandas as pd

# 파일 경로 (같은 디렉토리에 위치해야 함)
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 불러오기
try:
    df = pd.read_csv(FILE_PATH, encoding='euc-kr')
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# '2025년05월_계_'로 시작하는 연령별 인구 컬럼만 선택
age_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]

# 연령 숫자만 추출하여 열 이름 변경
renamed_cols = {col: col.split('_')[-1].replace('세', '') for col in age_cols}
df.rename(columns=renamed_cols, inplace=True)

# 총인구수 기준 상위 5개 행정구역 추출
top5_df = df.sort_values(by='총인구수', ascending=False).head(5)

# 시각화를 위한 데이터 변형
age_numbers = list(renamed_cols.values())
chart_df = top5_df[age_numbers].transpose()
chart_df.columns = top5_df['행정구역(동읍면)별']
chart_df.index.name = '연령'

# 선 그래프 출력
st.subheader("📊 상위 5개 지역 연령별 인구 비교 (선 그래프)")
st.line_chart(chart_df)

# 원본 데이터 출력
st.subheader("🗃 원본 데이터 (전체)")
st.dataframe(df)
