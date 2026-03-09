import pytest
from unittest.mock import MagicMock, patch

from pyconnectors.config import ConnectorConfig
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
