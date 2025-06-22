import sys
sys.path.append('/opt/airflow')

from dotenv import load_dotenv
import os
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from datetime import datetime, timedelta
import pendulum
from etl_utils.fetch_subway_loc_api import fetch_subway_loc_api
from etl_utils.fetch_subway_user_api import fetch_subway_user_api
from etl_utils.merge_dataset import merge_dataset

@task
def compute_target_date():
    context = get_current_context()
    date = (context["data_interval_start"] - timedelta(days=4)).strftime("%Y%m%d")
    return date

@task
def fetch_subway_user(API_KEY: str, now: str, path: str):
  return fetch_subway_user_api(
    api_key=API_KEY,
    date=now,
    parquet_path=path
  )

@task
def fetch_subway_loc(API_KEY: str, now: str, path: str):
  return fetch_subway_loc_api(
    api_key=API_KEY,
    date=now,
    parquet_path=path
  )

@task
def merge_and_save_parquet(user: str, loc: str, now: str, path: str):
  merge_dataset(
    user_parquet_path=user,
    loc_parquet_path=loc,
    date=now,
    output_parquet_path=path
  )

default_args = {
  'retries': 1,
  'retry_delay': timedelta(minutes=5),
  'start_date': datetime(2025, 6, 1, tzinfo=pendulum.timezone('Asia/Seoul'))
}

@dag(
  dag_id='subway_api_4days_behind_to_s3',
  default_args=default_args,
  schedule_interval='0 0 * * *',
  catchup=False,
  tags=['subway']
)
def subway_etl():
  load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../configs/.env'))
  API_KEY = os.getenv('API_KEY')

  user_path = '/opt/airflow/data/raw/user/'
  loc_path = '/opt/airflow/data/raw/loc/'
  merged_path = '/opt/airflow/data/merged/'

  now = compute_target_date()
  user = fetch_subway_user(API_KEY=API_KEY, now=now, path=user_path)
  loc = fetch_subway_loc(API_KEY=API_KEY, now=now, path=loc_path)
  merge_and_save_parquet(user=user, loc=loc, now=now, path=merged_path)

subway_etl()