from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="일본 여행, 몇 월에 가면 좋을까?", page_icon="🌸")

# CSV에서 세 도시의 데이터만 가져옵니다.
data = pd.read_csv(Path(__file__).parent / "data" / "climate.csv")
cities = ["도쿄", "오사카", "삿포로"]
data = data[data["city"].isin(cities)]

st.title("🌸 일본 여행, 몇 월에 가면 좋을까?")
st.write("도쿄, 오사카, 삿포로의 기온과 강수량을 비교해 보세요.")

st.subheader("선택한 도시의 월별 기온")
city = st.selectbox("궁금한 도시를 선택하세요", cities)
city_data = data[data["city"] == city]

# 선택한 도시의 평균기온을 선 그래프로 그립니다.
temperature_chart = px.line(
    city_data, x="month", y="temperature_c", markers=True,
    labels={"month": "월", "temperature_c": "평균기온 (°C)"},
)
temperature_chart.update_traces(line_color="#D64C45")
temperature_chart.update_xaxes(dtick=1)
temperature_chart.update_layout(margin=dict(t=15, b=10), height=320)
st.plotly_chart(temperature_chart, width="stretch", config={"displayModeBar": False})

warmest = city_data.loc[city_data["temperature_c"].idxmax()]
st.write(f"{city}는 평균적으로 **{int(warmest['month'])}월**이 가장 따뜻해요. 평균기온은 **{warmest['temperature_c']:.1f}°C**입니다.")

st.divider()
st.subheader("여행할 달의 강수량 비교")
month = st.slider("몇 월에 여행하고 싶나요?", 1, 12, 5)
month_data = data[data["month"] == month]
st.caption("이 그래프는 위에서 고른 도시와 관계없이 세 도시를 모두 비교합니다.")

# 선택한 달의 강수량을 도시별로 비교합니다.
rain_chart = px.bar(
    month_data, x="city", y="precipitation_mm", text_auto=".1f",
    labels={"city": "도시", "precipitation_mm": "월 강수량 (mm)"},
    category_orders={"city": cities},
)
rain_chart.update_traces(marker_color="#65A7C6")
rain_chart.update_layout(margin=dict(t=15, b=10), height=320)
st.plotly_chart(rain_chart, width="stretch", config={"displayModeBar": False})

driest = month_data.loc[month_data["precipitation_mm"].idxmin()]
st.write(f"**{month}월**에는 세 도시 중 **{driest['city']}**의 월 강수량이 가장 적어요. (**{driest['precipitation_mm']:.1f}mm**)")

st.divider()
st.subheader(f"{city}의 월별 데이터")
table = city_data[["month", "temperature_c", "precipitation_mm"]].rename(
    columns={"month": "월", "temperature_c": "평균기온 (°C)", "precipitation_mm": "강수량 (mm)"}
)
st.dataframe(table, hide_index=True, width="stretch")

st.caption("출처: 일본 기상청(JMA)의 1991–2020년 평년값. 장기간의 평균적인 기후이며 실제 여행 날짜의 일기예보는 아닙니다. 강수량은 비 올 확률과 다릅니다.")
st.markdown("[일본 기상청 원본 데이터 보기](https://www.data.jma.go.jp/stats/data/en/normal/normal.html)")
