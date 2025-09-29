import streamlit as st
import pandas as pd
import altair as alt

# 앱 제목
st.title("🌍 MBTI 유형별 평균 비율 TOP 10")

# CSV 파일 불러오기 (같은 폴더에 있어야 함)
df = pd.read_csv("countriesMBTI_16types.csv")

# 'Country' 열 제외하고 MBTI 유형별 평균 계산
mbti_means = df.drop(columns=["Country"]).mean().sort_values(ascending=False).reset_index()
mbti_means.columns = ["MBTI", "Average_Percentage"]

# 상위 10개 추출
top10 = mbti_means.head(10)

# Altair 막대 그래프 생성
chart = (
    alt.Chart(top10)
    .mark_bar(color="#4B9CD3")
    .encode(
        x=alt.X("MBTI:N", sort="-y", title="MBTI 유형"),
        y=alt.Y("Average_Percentage:Q", title="평균 비율"),
        tooltip=["MBTI", alt.Tooltip("Average_Percentage:Q", format=".3f")]
    )
    .properties(
        width=700,
        height=400,
        title="🌟 MBTI 유형별 평균 비율 TOP 10"
    )
)

# 그래프 출력
st.altair_chart(chart, use_container_width=True)

# 데이터 미리보기 (선택사항)
with st.expander("📊 원본 데이터 일부 보기"):
    st.dataframe(df.head())
