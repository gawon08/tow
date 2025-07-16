import streamlit as st
import pandas as pd

st.title("2025년 5월 기준 연령별 인구 현황 시각화")

# 파일 경로
FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# CSV 읽기 (EUC-KR 또는 UTF-8 자동 시도)
try:
    try:
        df = pd.read_csv(FILE_PATH, encoding='euc-kr')
    except:
        df = pd.read_csv(FILE_PATH, encoding='utf-8')
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 연령별 인구 컬럼 추출 및 이름 정제
age_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
renamed_cols = {col: col.split('_')[-1].replace('세', '') for col in age_cols}
df.rename(columns=renamed_cols, inplace=True)

# 상위 5개 지역 선택
if '총인구수' not in df.columns:
    st.error("'총인구수' 컬럼을 찾을 수 없습니다.")
    st.dataframe(df.head())  # 컬럼 구조 보여주기
    st.stop()

top5_df = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령 데이터 추출 및 전치
age_numbers = list(renamed_cols.values())
chart_df = top5_df[age_numbers].transpose()
chart_df.columns = top5_df['행정구역(동읍면)별']
chart_df.index.name = '연령'

# 시각화
st.subheader("📊 상위 5개 지역의 연령별 인구 (선 그래프)")
st.line_chart(chart_df)

# 원본 데이터 표시
st.subheader("🗃 원본 데이터")
st.dataframe(df)
