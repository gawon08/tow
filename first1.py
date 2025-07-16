import streamlit as st
import pandas as pd
import os

# 파일 경로 (Streamlit 앱이 실행되는 디렉토리 기준)
FILE_PATH = "/mnt/data/202505_202505_연령별인구현황_월간.csv"

st.title("2025년 5월 연령별 인구 현황 분석")

# 파일 존재 여부 확인
if os.path.exists(FILE_PATH):
    # CSV 파일 불러오기
    df = pd.read_csv(FILE_PATH, encoding='euc-kr')

    # 총인구수 컬럼 자동 추출
    total_pop_col = [col for col in df.columns if col.startswith("2025년05월_계_총인구수")][0]
    df["총인구수"] = df[total_pop_col].astype(str).str.replace(",", "").astype(int)

    # 연령별 컬럼 추출 및 정리
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    age_rename = {col: col.replace("2025년05월_계_", "").replace("세", "").replace(" ", "") for col in age_cols}
    df_age = df[["행정구역", "총인구수"] + age_cols].rename(columns=age_rename)

    # 총인구수 기준 상위 5개 지역
    top5_df = df_age.sort_values(by="총인구수", ascending=False).head(5)

    # Melt하여 연령별 인구 시각화 준비
    top5_melted = top5_df.melt(id_vars=["행정구역", "총인구수"], var_name="연령", value_name="인구")
    top5_melted["인구"] = top5_melted["인구"].astype(str).str.replace(",", "").replace("nan", "0").astype(int)
    top5_melted["연령"] = top5_melted["연령"].astype(int)

    # 원본 데이터 일부 출력
    st.subheader("📄 원본 데이터 (일부 열만 표시)")
    st.dataframe(df.iloc[:, :15])

    # 시각화: 연령별 인구 선 그래프
    st.subheader("📊 상위 5개 지역 연령별 인구 변화")

    for region in top5_melted["행정구역"].unique():
        region_df = top5_melted[top5_melted["행정구역"] == region].sort_values(by="연령")
        st.write(f"### {region}")
        st.line_chart(region_df.set_index("연령")[["인구"]])
else:
    st.error(f"❌ 파일이 존재하지 않습니다: `{FILE_PATH}`")
