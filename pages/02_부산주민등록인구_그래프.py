import streamlit as st
import pandas as pd

# 제목
st.title("2025년 6월 기준 연령별 인구 현황")

# CSV 파일 불러오기 (EUC-KR 인코딩)
df = pd.read_csv("202506_202506_주민등록인구및세대현황_월간.csv", encoding='euc-kr')

# 연령별 인구 컬럼만 추출
age_columns = [col for col in df.columns if col.startswith('2025년06월_계_') and ('세' in col or '100세 이상' in col)]

# 컬럼 이름 변환 (보기 쉽게)
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년06월_계_', '').replace('세', '') + '세')

# 연령별 데이터프레임 구성
df_age = df[['행정구역'] + age_columns].copy()
df_age.columns = ['행정구역'] + new_columns

# 상위 5개 행정구역 추출 (총인구수가 없으므로 가나다순 기준)
top5_df = df_age.head(5)

# 📊 원본 데이터 출력
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)

# 📈 연령별 인구 선그래프 출력
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")
age_columns_only = top5_df.columns[1:]

for index, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    age_data = row[1:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
