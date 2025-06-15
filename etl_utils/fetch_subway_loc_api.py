import requests
import pandas as pd
from pathlib import Path

"""
  https://data.seoul.go.kr/dataList/OA-21232/S/1/datasetView.do
  서울시 역사마스터 정보에서 역명, 위도, 경도 추출
"""
def fetch_subway_loc_api(api_key: str, date: str, parquet_path: str):
  url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/subwayStationMaster/1/1000/"

  response = requests.get(url)
  response.raise_for_status()
  
  data = response.json()
  
  df = pd.DataFrame(data['subwayStationMaster']['row'])
  df = df[['BLDN_NM', 'LAT', 'LOT']]

  output_path = Path(parquet_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  df.to_parquet(f"{parquet_path}/{date}_station.parquet", index=False)