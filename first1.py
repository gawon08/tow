import streamlit as st
import pandas as pd
import os

# 앱 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 파일 경로 지정
file_path = "202505_202505_연령별인구현황_월간.csv"

# 파일 존재 여부 확인
if not os.path.exists(file_path):
    st.error(f"'{file_path}' 파일이 현재 디렉토리에 존재하지 않습니다.")
else:
    # CSV 파일 읽기
    df = pd.read_csv(file_path, encoding='euc-kr')

    # '총인구수' 컬럼 확인
    total_pop_col = '총인구수'

    # 연령별 인구 컬럼 필터링
    age_cols = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
    renamed_cols = {col: col.split('_')[-1].replace('세', '') for col in age_cols}
    df = df.rename(columns=renamed_cols)

    # 상위 5개 행정구역 추출
    df_top5 = df.sort_values(by=total_pop_col, ascending=False).head(5)

    # 연령별 데이터 변환
    age_only = list(renamed_cols.values())  # 연령 숫자만
    chart_data = df_top5[age_only].transpose()
    chart_data.columns = df_top5['행정구역(동읍면)별']
    chart_data.index.name = '연령'

    # 시각화
    st.subheader("📈 연령별 인구 추이 (상위 5개 행정구역)")
    st.line_chart(chart_data)

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터")
    st.dataframe(df)
