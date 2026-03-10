import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
from pyconnectors.connectors.storage.adls import ADLSConnector
from pyconnectors.connectors.storage.azure_blob import AzureBlobConnector
from pyconnectors.connectors.storage.cloudinary import CloudinaryConnector
from pyconnectors.connectors.storage.digitalocean import DigitalOceanSpaceConnector
from pyconnectors.connectors.storage.gcs import GCSConnector
from pyconnectors.connectors.storage.hetzner import HetznerConnector
from pyconnectors.connectors.storage.minio import MinioConnector
from pyconnectors.connectors.storage.ovh import OVHConnector
from pyconnectors.connectors.storage.s3 import S3Connector


@pytest.fixture
def s3_connector():
    config = ConnectorConfig(
        params={
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
            "region_name": "us-east-1",
        }
    )
    return S3Connector(config)


@patch("pyconnectors.connectors.storage.s3.boto3")
def test_s3_connector_put(mock_boto3, s3_connector):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    result = s3_connector.execute("put", "my-bucket", "test.txt", b"hello world")

    assert result == {"status": "uploaded"}
    mock_boto3.client.assert_called_with(
        "s3", aws_access_key_id="key", aws_secret_access_key="secret", region_name="us-east-1"
    )
    mock_client.put_object.assert_called_with(
        Bucket="my-bucket", Key="test.txt", Body=b"hello world"
    )


@patch("pyconnectors.connectors.storage.s3.boto3")
def test_s3_connector_get(mock_boto3, s3_connector):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    mock_response = {"Body": MagicMock()}
    mock_response["Body"].read.return_value = b"hello world"
    mock_client.get_object.return_value = mock_response

    result = s3_connector.execute("get", "my-bucket", "test.txt")

    assert result == {"status": "downloaded", "data": b"hello world"}
    mock_client.get_object.assert_called_with(Bucket="my-bucket", Key="test.txt")


@patch("pyconnectors.connectors.storage.gcs.storage")
def test_gcs_connector_execute(mock_storage):
    if mock_storage is None:
        pytest.skip("google-cloud-storage not available")

    config = ConnectorConfig(params={"project": "my-project"})
    connector = GCSConnector(config)

    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_blob = MagicMock()

    mock_storage.Client.return_value = mock_client
    mock_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    result = connector.execute("upload", "my-bucket", "test.txt", data="hello world")

    assert result == {"status": "uploaded"}
    mock_storage.Client.assert_called_with(project="my-project")
    mock_client.bucket.assert_called_with("my-bucket")
    mock_bucket.blob.assert_called_with("test.txt")
    mock_blob.upload_from_string.assert_called_with("hello world")


@patch("pyconnectors.connectors.storage.azure_blob.BlobServiceClient")
def test_azure_blob_connector_execute(mock_blob_service):
    if mock_blob_service is None:
        pytest.skip("azure-storage-blob not available")

    config = ConnectorConfig(params={"connection_string": "DefaultEndpointsProtocol=https;..."})
    connector = AzureBlobConnector(config)

    mock_client = MagicMock()
    mock_blob_client = MagicMock()

    mock_blob_service.from_connection_string.return_value = mock_client
    mock_client.get_blob_client.return_value = mock_blob_client

    result = connector.execute("upload", "my-container", "test.txt", data=b"hello world")

    assert result == {"status": "uploaded"}
    mock_blob_service.from_connection_string.assert_called_with(
        "DefaultEndpointsProtocol=https;..."
    )
    mock_client.get_blob_client.assert_called_with(container="my-container", blob="test.txt")
    mock_blob_client.upload_blob.assert_called_with(b"hello world", overwrite=True)


@patch("pyconnectors.connectors.storage.adls.DataLakeServiceClient")
def test_adls_connector_execute(mock_adls_service):
    if mock_adls_service is None:
        pytest.skip("azure-storage-file-datalake not available")

    config = ConnectorConfig(params={"connection_string": "DefaultEndpointsProtocol=https;..."})
    connector = ADLSConnector(config)

    mock_client = MagicMock()
    mock_fs_client = MagicMock()
    mock_file_client = MagicMock()

    mock_adls_service.from_connection_string.return_value = mock_client
    mock_client.get_file_system_client.return_value = mock_fs_client
    mock_fs_client.get_file_client.return_value = mock_file_client

    result = connector.execute("upload", "my-fs", "test.txt", data=b"hello world")

    assert result == {"status": "uploaded"}
    mock_client.get_file_system_client.assert_called_with(file_system="my-fs")
    mock_fs_client.get_file_client.assert_called_with("test.txt")
    mock_file_client.upload_data.assert_called_with(b"hello world", overwrite=True)


@patch("pyconnectors.connectors.storage.cloudinary.cloudinary")
def test_cloudinary_connector_execute(mock_cloudinary):
    if mock_cloudinary is None:
        pytest.skip("cloudinary not available")

    config = ConnectorConfig(params={"cloud_name": "demo", "api_key": "123", "api_secret": "abc"})
    connector = CloudinaryConnector(config)

    mock_cloudinary.uploader.upload.return_value = {"secure_url": "https://res.cloudinary.com/..."}

    result = connector.execute("upload", "/tmp/image.jpg", public_id="my_image")

    assert result == {"status": "uploaded", "url": "https://res.cloudinary.com/..."}
    mock_cloudinary.config.assert_called_with(cloud_name="demo", api_key="123", api_secret="abc")
    mock_cloudinary.uploader.upload.assert_called_with("/tmp/image.jpg", public_id="my_image")


@patch("pyconnectors.connectors.storage.minio.boto3")
def test_minio_connector_execute(mock_boto3):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    config = ConnectorConfig(
        params={
            "endpoint_url": "http://localhost:9000",
            "aws_access_key_id": "minioadmin",
            "aws_secret_access_key": "minioadmin",
        }
    )
    connector = MinioConnector(config)

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    result = connector.execute("upload", "my-bucket", "test.txt", data=b"hello world")

    assert result == {"status": "uploaded"}
    mock_boto3.client.assert_called_with(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )
    mock_client.put_object.assert_called_with(
        Bucket="my-bucket", Key="test.txt", Body=b"hello world"
    )


@patch("pyconnectors.connectors.storage.digitalocean.boto3")
def test_digitalocean_connector_execute(mock_boto3):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    config = ConnectorConfig(
        params={
            "region_name": "sfo3",
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
        }
    )
    connector = DigitalOceanSpaceConnector(config)

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    result = connector.execute("upload", "my-space", "test.txt", data=b"hello world")

    assert result == {"status": "uploaded"}
    mock_boto3.client.assert_called_with(
        "s3",
        endpoint_url="https://sfo3.digitaloceanspaces.com",
        aws_access_key_id="key",
        aws_secret_access_key="secret",
    )
    mock_client.put_object.assert_called_with(
        Bucket="my-space", Key="test.txt", Body=b"hello world", ACL="private"
    )


@patch("pyconnectors.connectors.storage.hetzner.boto3")
def test_hetzner_connector_execute(mock_boto3):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    config = ConnectorConfig(
        params={
            "region_name": "fsn1",
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
        }
    )
    connector = HetznerConnector(config)

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    result = connector.execute("upload", "my-bucket", "test.txt", data=b"hello world")

    assert result == {"status": "uploaded"}
    mock_boto3.client.assert_called_with(
        "s3",
        endpoint_url="https://fsn1.your-objectstorage.com",
        aws_access_key_id="key",
        aws_secret_access_key="secret",
    )
    mock_client.put_object.assert_called_with(
        Bucket="my-bucket", Key="test.txt", Body=b"hello world"
    )


@patch("pyconnectors.connectors.storage.ovh.boto3")
def test_ovh_connector_execute(mock_boto3):
    if mock_boto3 is None:
        pytest.skip("boto3 not available")

    config = ConnectorConfig(
        params={
            "region_name": "gra",
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
        }
    )
    connector = OVHConnector(config)

    mock_client = MagicMock()
    mock_boto3.client.return_value = mock_client

    result = connector.execute("upload", "my-bucket", "test.txt", data=b"hello world")

    assert result == {"status": "uploaded"}
    mock_boto3.client.assert_called_with(
        "s3",
        endpoint_url="https://s3.gra.perf.cloud.ovh.net",
        aws_access_key_id="key",
        aws_secret_access_key="secret",
    )
    mock_client.put_object.assert_called_with(
        Bucket="my-bucket", Key="test.txt", Body=b"hello world"
    )
