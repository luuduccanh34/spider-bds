# gcs_utils.py
# Utility functions for interacting with Google Cloud Storage

from google.cloud import storage
from variables.google_authentication import GoogleAuthentication
from variables.helper import ConfigLoader
import json
import logging
import pandas as pd
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GCSClient:
    """
    A client for interacting with Google Cloud Storage.

    Attributes:
        client (google.cloud.storage.Client): The Google Cloud Storage client instance.
    """

    def __init__(self):
        logging.info("Initializing GCSClient...")
        logging.info("Loading Google Cloud configuration...")
        gcp_config = ConfigLoader.load_single(GoogleAuthentication)
        logging.info("Google Cloud configuration loaded: %s", gcp_config)

        try:
            service_account_info = json.loads(gcp_config['GOOGLE_SERVICE_ACCOUNT'])
            self.client = storage.Client.from_service_account_info(service_account_info)
            logging.info("Google Cloud Storage client initialized successfully.")
        except json.JSONDecodeError as e:
            logging.error("Failed to parse service account text: %s", e)
            raise
        except Exception as e:
            logging.error("Failed to initialize Google Cloud Storage client: %s", e)
            raise

    def list_buckets(self):
        """
        Lists all buckets in the Google Cloud Storage project.

        Returns:
            list: A list of bucket names.
        """
        logging.info("Listing all buckets...")
        try:
            buckets = [bucket.name for bucket in self.client.list_buckets()]
            logging.info("Buckets retrieved: %s", buckets)
            return buckets
        except Exception as e:
            logging.error("Failed to list buckets: %s", e)
            raise

    def upload_file(self, source_file_name, bucket_name, destination_blob_name):
        """
        Uploads a file to a specified bucket in Google Cloud Storage.

        Args:
            source_file_name (str): The path to the source file to upload.
            bucket_name (str): The name of the destination bucket.
            destination_blob_name (str): The name of the destination blob in the bucket.
        """
        logging.info("Uploading file '%s' to bucket '%s' as '%s'...", source_file_name, bucket_name, destination_blob_name)
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
            logging.info("File '%s' uploaded to '%s'.", source_file_name, destination_blob_name)
        except Exception as e:
            logging.error("Failed to upload file '%s': %s", source_file_name, e)
            raise

    def download_file(self, bucket_name, prefix, file_format, mode='single', source_blob_name=None, destination_file_name=None):
        """
        Downloads files from a specified bucket in Google Cloud Storage.

        Args:
            bucket_name (str): The name of the source bucket.
            prefix (str): The prefix (folder path) in the bucket.
            file_format (str): The format of the files to download (e.g., 'csv', 'json', 'parquet').
            mode (str): The mode of download. 'single' for a specific file, 'full' to download all files with the specified format under the prefix.
            source_blob_name (str, optional): The name of the source blob in the bucket (required for 'single' mode).
            destination_file_name (str, optional): The path to save the downloaded file (required for 'single' mode).
        """
        logging.info("Downloading files from bucket '%s' with prefix '%s' in mode '%s'...", bucket_name, prefix, mode)
        try:
            bucket = self.client.bucket(bucket_name)

            if mode == 'single':
                if not source_blob_name:
                    raise ValueError("'source_blob_name' is required for 'single' mode.")

                if not destination_file_name:
                    # Set default destination path
                    os.makedirs('data_downloaded', exist_ok=True)
                    destination_file_name = os.path.join('data_downloaded', source_blob_name.split('/')[-1])

                blob = bucket.blob(source_blob_name)
                blob.download_to_filename(destination_file_name)
                logging.info("Blob '%s' downloaded to '%s'.", source_blob_name, destination_file_name)

            elif mode == 'full':
                if not destination_file_name:
                    # Set default destination folder
                    os.makedirs('data_downloaded', exist_ok=True)
                    destination_file_name = 'data_downloaded'

                blobs = bucket.list_blobs(prefix=prefix)
                for blob in blobs:
                    if blob.name.endswith(f".{file_format}"):
                        destination_path = os.path.join(destination_file_name, blob.name.split('/')[-1])
                        blob.download_to_filename(destination_path)
                        logging.info("Blob '%s' downloaded to '%s'.", blob.name, destination_path)

            else:
                raise ValueError("Unsupported mode. Supported modes are: 'single', 'full'.")

        except Exception as e:
            logging.error("Failed to download files: %s", e)
            raise

    def upload_dataframe(self, bucket_name, prefix, dataframe, file_name=None, file_format='csv'):
        """
        Uploads a Pandas DataFrame directly to a specified bucket in Google Cloud Storage in the specified format.

        Args:
            bucket_name (str): The name of the destination bucket.
            prefix (str): The prefix (folder path) in the bucket.
            dataframe (pd.DataFrame): The DataFrame to upload.
            file_name (str, optional): The base name of the file to store in the bucket. Defaults to None.
            file_format (str, optional): The format of the file to store (csv, parquet, json). Defaults to 'csv'.

        Returns:
            str: The full path of the uploaded file in the bucket.
        """
        logging.info("Uploading DataFrame to bucket '%s' with prefix '%s' directly in format '%s'...", bucket_name, prefix, file_format)
        try:
            # Validate file format
            if file_format not in ['csv', 'parquet', 'json']:
                raise ValueError("Unsupported file format. Supported formats are: csv, parquet, json.")

            # Generate file name with timestamp
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            if file_name:
                full_file_name = f"{file_name}_{current_time}.{file_format}"
            else:
                full_file_name = f"{current_time}.{file_format}"

            # Initialize variables
            data = None
            content_type = None

            # Convert DataFrame to the specified format
            if file_format == 'csv':
                data = dataframe.to_csv(index=False)
                content_type = "text/csv"
            elif file_format == 'parquet':
                import io
                buffer = io.BytesIO()
                dataframe.to_parquet(buffer, index=False, engine='pyarrow')
                buffer.seek(0)
                data = buffer.read()
                content_type = "application/octet-stream"
            elif file_format == 'json':
                data = dataframe.to_json(orient='records')
                content_type = "application/json"

            # Upload the data directly to GCS
            destination_blob_name = f"{prefix}/{full_file_name}"
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_string(data, content_type=content_type)

            logging.info("DataFrame uploaded directly to '%s/%s'.", bucket_name, destination_blob_name)
            return destination_blob_name
        except Exception as e:
            logging.error("Failed to upload DataFrame directly: %s", e)
            raise
