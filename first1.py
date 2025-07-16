import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# 고정된 파일 경로
file_path = "/mnt/data/202505_202505_연령별인구현황_월간.csv"

# CSV 불러오기
df = pd.read_csv(file_path, encoding='euc-kr')

# 총인구수 컬럼 추출
total_pop_col = [col for col in df.columns if "2025년05월_계_총인구수" in col][0]
df["총인구수"] = df[total_pop_col].astype(str).str.replace(",", "").astype(int)

# 연령별 컬럼 필터링
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
age_col_map = {col: col.replace("2025년05월_계_", "").replace("세", "").strip() for col in age_cols}

# 필요한 데이터 정리
df_age = df[["행정구역", "총인구수"] + age_cols].rename(columns=age_col_map)

# 총인구수 기준 상위 5개 지역 선정
top5_df = df_age.sort_values(by="총인구수", ascending=False).head(5)

# Melt: 연령별 인구 분포 그래프용
melted = top5_df.melt(id_vars=["행정구역", "총인구수"], var_name="연령", value_name="인구")
melted["인구"] = melted["인구"].astype(str).str.replace(",", "").replace("nan", "0").astype(int)
melted["연령"] = melted["연령"].astype(int)

# 데이터 일부 미리 보기
st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df.iloc[:, :15])

# 시각화
st.subheader("📈 상위 5개 지역의 연령별 인구 분포")

for region in melted["행정구역"].unique():
    region_df = melted[melted["행정구역"] == region].sort_values(by="연령")
    st.write(f"### {region}")
    st.line_chart(region_df.set_index("연령")[["인구"]])
