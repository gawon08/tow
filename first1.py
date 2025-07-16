import streamlit as st
import pandas as pd

# CSV 파일 업로드
st.title("2025년 5월 기준 연령별 인구 현황")
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    # CSV 불러오기
    df = pd.read_csv(uploaded_file, encoding="euc-kr")

    # 총인구수 컬럼 정리
    df["총인구수"] = df["2025년05월_계_총인구수"].str.replace(",", "").astype(int)

    # 연령 관련 컬럼 추출
    age_cols = [col for col in df.columns if col.startswith("2025년05월_계_") and "세" in col]
    age_rename = {col: col.replace("2025년05월_계_", "").replace("세", "").replace(" ", "") for col in age_cols}
    df_renamed = df[["행정구역", "총인구수"] + age_cols].rename(columns=age_rename)

    # 총인구수 상위 5개 행정구역 추출
    top5_df = df_renamed.sort_values(by="총인구수", ascending=False).head(5)

    # 연령별 인구 데이터를 세로로 변환
    df_melted = top5_df.melt(id_vars=["행정구역", "총인구수"], var_name="연령", value_name="인구")
    df_melted["인구"] = (
        df_melted["인구"]
        .astype(str)
        .str.replace(",", "")
        .replace("nan", "0")
        .astype(int)
    )

    # Streamlit line chart로 시각화
    st.subheader("연령별 인구 분포 (상위 5개 행정구역)")
    for region in df_melted["행정구역"].unique():
        region_data = df_melted[df_melted["행정구역"] == region]
        region_data_sorted = region_data.sort_values(by="연령", key=lambda x: x.astype(int))
        st.line_chart(
            data=region_data_sorted.set_index("연령")["인구"],
            use_container_width=True,
            height=300
        )
        st.caption(f"📍 {region}의 연령별 인구 변화")

    # 원본 데이터 표시
    st.subheader("원본 데이터 미리보기")
    st.dataframe(df)
