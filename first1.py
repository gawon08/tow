import streamlit as st
import pandas as pd

st.title("2025년 5월 기준 연령별 인구 현황 시각화")

FILE_PATH = "202505_202505_연령별인구현황_월간.csv"

# CSV 파일 읽기
try:
    try:
        df = pd.read_csv(FILE_PATH, encoding='euc-kr')
    except:
        df = pd.read_csv(FILE_PATH, encoding='utf-8')
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 열 이름 공백 제거
df.columns = df.columns.str.strip()

# 실제 컬럼 이름 확인 (디버그용)
st.write("✅ 현재 데이터 컬럼:", df.columns.tolist())

# 연령별 인구 열 추출 및 이름 정리
age_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
renamed_cols = {col: col.split('_')[-1].replace('세', '') for col in age_cols}
df.rename(columns=renamed_cols, inplace=True)

# '총인구수' 열이 실제 존재하는지 확인
if '총인구수' not in df.columns:
    st.error("'총인구수' 컬럼을 찾을 수 없습니다. 실제 컬럼명을 확인해주세요.")
    st.dataframe(df.head())
    st.stop()

# 상위 5개 지역 추출
top5_df = df.sort_values(by='총인구수', ascending=False).head(5)

# 연령 그래프 데이터 구성
age_numbers = list(renamed_cols.values())
chart_df = top5_df[age_numbers].transpose()
chart_df.columns = top5_df['행정구역(동읍면)별']
chart_df.index.name = '연령'

# 시각화
st.subheader("📈 상위 5개 지역의 연령별 인구")
st.line_chart(chart_df)

# 원본 데이터 표시
st.subheader("🗃 원본 데이터")
st.dataframe(df)
