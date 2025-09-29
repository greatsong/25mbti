import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="MBTI by Country", page_icon="🌐", layout="centered")

st.title("🌐 나라별 MBTI 분포 대시보드")
st.caption("원하는 나라를 선택하면 MBTI 유형 분포를 한눈에 볼 수 있어요. ✨")

# 데이터 불러오기 (동일 폴더)
df = pd.read_csv("countriesMBTI_16types.csv")

# MBTI 컬럼 목록 (Country 제외)
mbti_cols = [c for c in df.columns if c != "Country"]

# 사이드바 - 나라 선택
st.sidebar.header("🔎 필터")
countries = sorted(df["Country"].unique().tolist())
country = st.sidebar.selectbox("나라 선택", countries, index=0)

# 선택한 나라의 데이터 가공
row = df[df["Country"] == country].iloc[0]
data = (
    pd.DataFrame({"MBTI": mbti_cols, "Percentage": [row[c] for c in mbti_cols]})
    .sort_values("Percentage", ascending=False)
    .reset_index(drop=True)
)

# 상단 하이라이트 (TOP 3)
st.subheader(f"🏳️ {country} — 상위 3개 MBTI")
top3 = data.head(3)
c1, c2, c3 = st.columns(3)
for col, (mbti, pct) in zip([c1, c2, c3], zip(top3["MBTI"], top3["Percentage"])):
    col.metric(label=f"🔥 {mbti}", value=f"{pct:.1%}")

# 보기 좋은 색상 팔레트 (파스텔 톤)
palette = [
    "#7FB3D5", "#A9DFBF", "#F7DC6F", "#F5B7B1",
    "#C39BD3", "#AED6F1", "#F8C471", "#82E0AA",
    "#F1948A", "#BB8FCE", "#76D7C4", "#F0B27A",
    "#85C1E9", "#F5CBA7", "#D2B4DE", "#A3E4D7",
]

# Plotly 막대그래프
fig = px.bar(
    data,
    x="MBTI",
    y="Percentage",
    color="MBTI",
    color_discrete_sequence=palette,
    title=f"📊 {country}의 MBTI 분포",
    hover_data={"MBTI": True, "Percentage": ":.2%"},
)

fig.update_traces(
    texttemplate="%{y:.1%}",
    textposition="outside",
)

fig.update_layout(
    yaxis_tickformat=".0%",
    xaxis_title="MBTI 유형",
    yaxis_title="비율",
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=20),
)

st.plotly_chart(fig, use_container_width=True)

# 원본표 미리보기
with st.expander("📄 선택한 나라의 원본 값 보기"):
    show = data.copy()
    show["Percentage"] = show["Percentage"].map(lambda v: f"{v:.2%}")
    st.dataframe(show, use_container_width=True)

st.caption("💡 팁: 막대 위 수치를 참고하고, 툴팁(hover)으로 소수점 두 자리까지 확인해보세요.")
