import streamlit as st
import pandas as pd

# 앱 제목
st.title("2025년 6월 기준 연령별 인구 현황")

# CSV 파일 직접 읽기
df = pd.read_csv("202506_202506_주민등록인구및세대현황_월간.csv", encoding='euc-kr')

# 연령별 인구 컬럼 필터링
# "2025년06월_계_"로 시작하고 '세' 또는 '100세 이상'이 포함된 열만 선택
age_columns = [col for col in df.columns if col.startswith('2025년06월_계_') and ('세' in col or '100세 이상' in col)]

# 총인구수 컬럼 전처리 (쉼표 제거 후 정수형 변환)
df['총인구수'] = df['2025년06월_계_총인구수'].str.replace(',', '').astype(int)

# 나이 컬럼명 정제
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년06월_계_', '').replace('세', '') + '세')

# 필요한 열만 추출
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 총인구수 기준 상위 5개 지역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 📊 원본 데이터 출력
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df)

# 📈 연령별 인구 선그래프
st.subheader("📈 상위 5개 행정구역 연령별 인구 분포")

age_columns_only = top5_df.columns[2:]

for index, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    age_data = row[2:].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
