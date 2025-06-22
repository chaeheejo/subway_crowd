import requests
import pandas as pd
from pathlib import Path

"""
  https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do
  서울시 지하철호선별 역별 승하차 인원 정보에서 역명, 승/하차 인원 추출
"""  
def fetch_subway_user_api(api_key: str, date: str, parquet_path: str):
  url = f"http://openapi.seoul.go.kr:8088/{api_key}/json/CardSubwayStatsNew/1/1000/{date}"

  response = requests.get(url)
  response.raise_for_status()

  data = response.json()
  
  df = pd.DataFrame(data['CardSubwayStatsNew']['row'])
  df = df[['SBWY_STNS_NM', 'GTON_TNOPE', 'GTOFF_TNOPE']]

  output_path = Path(parquet_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)

  file_path = parquet_path + f"{date}_user.parquet"
  df.to_parquet(file_path, index=False)

  return file_path