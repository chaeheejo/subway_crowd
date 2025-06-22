import pandas as pd
from pathlib import Path

def merge_dataset(user_parquet_path: str, loc_parquet_path: str, date: str, output_parquet_path: str):
  user_df = pd.read_parquet(user_parquet_path)
  user_df = user_df.rename(columns={'SBWY_STNS_NM': 'STATION_NM'})

  loc_df = pd.read_parquet(loc_parquet_path)
  loc_df = loc_df.rename(columns={'BLDN_NM': 'STATION_NM'})

  merged_df = pd.merge(user_df, loc_df, on='STATION_NM', how='inner')

  merged_df = merged_df.rename(columns={'LAT': 'lat', 'LOT': 'lon'})
  merged_df['lat'] = pd.to_numeric(merged_df['lat'], errors='coerce')
  merged_df['lon'] = pd.to_numeric(merged_df['lon'], errors='coerce')
  merged_df['TOTAL'] = merged_df['GTON_TNOPE'].fillna(0) + merged_df['GTOFF_TNOPE'].fillna(0)
  merged_df = merged_df.dropna(subset=['lat', 'lon'])

  output_path = Path(output_parquet_path)
  output_path.parent.mkdir(parents=True, exist_ok=True)
  
  merged_df.to_parquet(output_parquet_path+f"{date}.parquet", index=False)