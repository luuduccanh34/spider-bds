import os
from utils.gcp.gcs_helper import GCSClient
import pandas as pd

def main():
    # Create a sample DataFrame
    df = pd.DataFrame({
        'name': ['Canh', 'Bob', 'Charlie'],
        'age': [25, 30, 35]
    })

    # Initialize GCSClient
    gcs_client = GCSClient()

    # Retrieve environment variables
    bucket_name = os.getenv('GCS_BUCKET_NAME', 'prod-dp')
    prefix = os.getenv('GCS_PREFIX', 'data_test_check')
    file_name = os.getenv('GCS_FILE_NAME', 'canhld')
    file_format = os.getenv('GCS_FILE_FORMAT', 'csv')

    # Upload the DataFrame
    gcs_client.upload_dataframe(bucket_name, prefix, df, file_name, file_format)

if __name__ == "__main__":
    main()
