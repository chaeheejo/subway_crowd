# subway_crowd
# 서울 지하철 이용객 시각화 프로젝트

서울 지하철 승하차 인원 데이터를 자동으로 수집, 전처리하고 시각화하는 Streamlit 기반 웹 애플리케이션입니다.

ETL 파이프라인은 Apache Airflow로 구성되어 있으며, 매일 수집된 데이터를 병합하여 Parquet 파일로 저장하고, Streamlit 앱에서 이를 시각화합니다.

---

## 📌 주요 기능

### 🚇 Streamlit 지도 시각화

- 일별 지하철 역 이용객 수 시각화 (승차 / 하차 / 총 이용객 수)
- Pydeck 기반 인터랙티브 지도 시각화
- 이용객 수에 따라 색상 차등 표현
- 날짜 선택 UI 제공

### 🔄 Airflow 기반 ETL 파이프라인

- 서울시 공공 API에서 승하차 및 역 위치 데이터 수집
- 날짜 기준 데이터 병합 및 Parquet 저장
- DAG 스케줄링을 통해 매일 자동 실행
- Streamlit 앱에서 바로 사용할 수 있는 데이터 구조 유지

---

## 🗂️ 프로젝트 구조

<pre><code>
project/
├── app.py # Streamlit 앱
├── dags/
│ └── dag.py # Airflow DAG
├── etl_utils/
│ ├── fetch_subway_user_api.py # 승/하차 API 추출 함수
│ ├── fetch_subway_loc_api.py # 역 위치 정보 API 추출 함수
│ └── merge_dataset.py # 데이터 병합 및 저장 함수
├── data/
│ └── merged/ # 병합된 일별 Parquet 데이터
│ └── raw/
│     └── loc/ #일자별 역 위치 정보
│     └── user/ #일자별 승/하차 데이터
└── configs/
  └── .env # API 키 저장용 환경변수 파일
</code></pre>


