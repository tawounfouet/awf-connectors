import os
from pyconnectors.config import ConnectorConfig
from pyconnectors.factory import ConnectorFactory

import pyconnectors.connectors.storage.s3  # noqa


def main():
    print("Storage Connectors Example - Amazon S3")

    # Check if boto3 is installed (since it's an optional dependency)
    try:
        import boto3  # noqa
    except ImportError:
        print("This example requires boto3. Please install it using `pip install pyconnectors[s3]`")
        return

    # To connect to AWS S3, you need IAM credentials.
    config = ConnectorConfig(
        params={
            "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", "mock_key"),
            "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", "mock_secret"),
            "region_name": "us-east-1",
        }
    )

    s3 = ConnectorFactory.create("storage.s3", config=config)

    # 1. Uploading a file (bytes)
    data_to_upload = b"Hello from PyConnectors! This is a test file."

    print("Attempting to upload data to S3...")
    result_upload = s3.safe_execute(
        action="upload", bucket="my-example-bucket", key="test_file.txt", data=data_to_upload
    )

    if result_upload.success:
        print("Upload successful!")
    else:
        print("Upload failed (Expected with mock credentials):", result_upload.error)

    # 2. Downloading a file
    print("\nAttempting to download data from S3...")
    result_download = s3.safe_execute(
        action="download", bucket="my-example-bucket", key="test_file.txt"
    )

    if result_download.success:
        print("Download successful!")
        print("Data:", result_download.data)
    else:
        print("Download failed:", result_download.error)


if __name__ == "__main__":
    main()
