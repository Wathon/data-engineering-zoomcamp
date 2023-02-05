from pathlib import Path
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials


@task(log_prints=True, retries=1)
def transform(path: Path) -> pd.DataFrame:
    """Data cleaning example"""
    df = pd.read_parquet(path)
    print(f"columns: {df.dtypes}")
    return df


@task(log_prints=True, retries=1)
def write_bq(df: pd.DataFrame) -> None:
    """Write Dataframe to BigQuery"""

    gcp_credentials_block = GcpCredentials.load("de-gcp")
    df.to_gbq(
        destination_table="trips_data_all.yellow_taxi_trips",
        project_id="dtc-de-375407",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append"
    )


@task(log_prints=True, retries=1)
def extract_from_gcs(color: str, year: int, month: int) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"./data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("de-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"./data/")
    return Path(f"./{gcs_path}")


@flow(name="ETL GCS to Big Query")
def etl_gcs_to_bq(year, month, color):
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(color, year, month)
    df = transform(path)
    write_bq(df)

@flow(name="etl-gcs-bq-parent-flow")
def etl_gcs_to_bq_parent_flow(months: list[int] = [2, 3], year: int = 2019, color: str = "yellow"):
    for month in months:
        etl_gcs_to_bq(year, month, color)

if __name__ == '__main__':
    etl_gcs_to_bq_parent_flow()
