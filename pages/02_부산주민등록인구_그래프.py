import streamlit as st
import pandas as pd

# 제목
st.title("2025년 6월 기준 부산광역시 연령별 인구 현황")

# CSV 파일 불러오기
df = pd.read_csv("202506_202506_주민등록인구및세대현황_월간.csv", encoding='euc-kr')

# 연령별 인구 컬럼 필터링
age_columns = [col for col in df.columns if col.startswith('2025년06월_계_') and ('세' in col or '100세 이상' in col)]

# 컬럼명 보기 좋게 정리
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년06월_계_', '').replace('세', '') + '세')

# 연령별 데이터프레임 구성
df_age = df[['행정구역'] + age_columns].copy()
df_age.columns = ['행정구역'] + new_columns

# 부산광역시 데이터만 필터링
busan_df = df_age[df_age['행정구역'].str.contains('부산광역시')].copy()

# 📊 데이터 확인
st.subheader("📊 부산광역시 원본 데이터")
st.dataframe(busan_df)

# 📈 그래프 그리기
st.subheader("📈 부산광역시 연령별 인구 분포")

age_columns_only = busan_df.columns[1:]

# 데이터가 존재할 때만 그래프 그리기
if not busan_df.empty:
    for index, row in busan_df.iterrows():
        st.write(f"### {row['행정구역']}")
        # 쉼표 제거 후 숫자 변환
        age_data = row[1:].astype(str).str.replace(',', '').astype(int)
        age_df = pd.DataFrame({
            '연령': age_columns_only,
            '인구수': age_data.values
        }).set_index('연령')
        st.line_chart(age_df)
else:
    st.warning("❗ 부산광역시 관련 데이터가 없습니다.")
