import streamlit as st
import pandas as pd
import pydeck as pdk
import glob
import re

st.title("서울 지하철 역 이용객수 지도")

files = glob.glob("./data/merged/*.parquet")
if not files:
  st.error("병합할 데이터가 없습니다.")
  st.stop()

parsing = re.compile(r"(\d{8})")
date_to_file = {}
dates = []
for file in files:
  match = parsing.search(file)
  if match:
    date_str = match.group(1)
    date_to_file[date_str] = file
    dates.append(date_str)
dates = sorted(dates)

date_display = [f"{d[:4]} / {d[4:6]} / {d[6:]}" for d in dates]
date_display_to_raw = dict(zip(date_display, dates))

selected_display = st.selectbox("날짜를 선택하세요", date_display)
selected_date = date_display_to_raw[selected_display]
selected_file = date_to_file[selected_date]

df = pd.read_parquet(selected_file)
df = df.rename(columns={'LAT': 'lat', 'LOT': 'lon'})

df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
df['TOTAL'] = df['GTON_TNOPE'].fillna(0) + df['GTOFF_TNOPE'].fillna(0)
df = df.dropna(subset=['lat', 'lon'])

value_option = st.radio(
  "지도에 표시할 값 선택",
  ("승차 인원수", "하차 인원수", "총 이용객수"),
  horizontal=True
)
if value_option == "승차 인원수":
  value_col = "GTON_TNOPE"
  value_label = "승차 인원"
  tooltip = {
    "text": "{STATION_NM}\n승차: {GTON_TNOPE}"
  }
elif value_option == "하차 인원수":
  value_col = "GTOFF_TNOPE"
  value_label = "하차 인원"
  tooltip = {
    "text": "{STATION_NM}\n하차: {GTOFF_TNOPE}"
  }
else:
  value_col = "TOTAL"
  value_label = "총 이용객수"
  tooltip = {
    "text": "{STATION_NM}\n이용객수: {TOTAL}"
  }

color_bins = [
  (0, 5000, [0, 120, 255, 180], '5,000명 미만'),            # 파랑
  (5000, 10000, [0, 200, 0, 180], '5,000~9,999명'),        # 초록
  (10000, 20000, [255, 230, 0, 180], '10,000~19,999명'),   # 노랑
  (20000, float('inf'), [255, 0, 60, 180], '20,000명 이상') # 빨강
]
def pick_color(val):
  for vmin, vmax, color, _ in color_bins:
    if vmin <= val < vmax:
      return color
  return [100, 100, 100, 180]  # 예외(회색)
df['color'] = df[value_col].apply(pick_color)

st.markdown("##### 색상 기준(이용객수)")
for _, _, color, label in color_bins:
  color_hex = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
  st.markdown(
    f'<div style="display:inline-block;width:18px;height:18px;background:{color_hex};margin-right:8px;border-radius:9px"></div>'
    f'{label}',
    unsafe_allow_html=True
  )

layer = pdk.Layer(
  "ScatterplotLayer",
  data=df,
  get_position='[lon, lat]',
  get_radius=f"{value_col} / 50",
  get_fill_color="color",
  pickable=True,
)

view_state = pdk.ViewState(
  latitude=37.5665,
  longitude=126.9780,
  zoom=10,
  pitch=0,
)

st.pydeck_chart(pdk.Deck(
  layers=[layer],
  initial_view_state=view_state,
  tooltip=tooltip
))