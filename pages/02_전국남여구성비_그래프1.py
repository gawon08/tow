import streamlit as st
import pandas as pd

st.title("2025년 6월 기준 연령별 남녀 인구 구성비 (상위 5개 지역)")

# 엑셀 파일 읽기
df = pd.read_excel("202506_202506_주민등록인구및세대현황_월간.xlsx", skiprows=2)

# '행정기관' NaN 제거
df = df[df['행정기관'].notna()]

# 남자/여자 열 추출
male_columns = [col for col in df.columns if '세' in str(col) and '남' in str(col)]
female_columns = [col for col in df.columns if '세' in str(col) and '여' in str(col)]

# 연령 이름 정리 (예: '0세 남' → '0세')
def clean_age(col):
    return col.split('세')[0].strip() + '세'

ages = [clean_age(col) for col in male_columns]

# 총 인구 계산 (남+여)
df['총합'] = df[male_columns + female_columns].sum(axis=1)

# 총합 기준 상위 5개 지역
top5_df = df.sort_values(by='총합', ascending=False).head(5)

# 📊 표 출력
st.subheader("📊 상위 5개 지역 남녀 연령별 인구 데이터")
for idx, row in top5_df.iterrows():
    region = row['행정기관']
    male_data = row[male_columns].astype(int).values
    female_data = row[female_columns].astype(int).values
    
    table_df = pd.DataFrame({
        '연령': ages,
        '남자': male_data,
        '여자': female_data
    })
    st.write(f"### {region}")
    st.dataframe(table_df)

# 📈 그래프 출력
st.subheader("📈 연령별 남녀 인구 그래프 (상위 5개 지역)")
for idx, row in top5_df.iterrows():
    region = row['행정기관']
    male_data = row[male_columns].astype(int).values
    female_data = row[female_columns].astype(int).values
    
    chart_df = pd.DataFrame({
        '연령': ages,
        '남자': male_data,
        '여자': female_data
    }).set_index('연령')
    
    st.write(f"### {region}")
    st.line_chart(chart_df)
