from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

# alternative to creating GCP blocks in the UI
# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!


credentials_block = GcpCredentials(
    # enter your credentials info or use the file method.
    service_account_info={}
)
credentials_block.save("de-gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("de-gcp-creds"),
    bucket="dtc_data_lake_dtc-de-375407",  # insert your  GCS bucket name
)

bucket_block.save("zoom-gcs", overwrite=True)
