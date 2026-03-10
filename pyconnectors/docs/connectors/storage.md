# Storage Connectors

Storage connectors allow files and blob data to be stored across a wide array of cloud vendors. We support native SDKs and S3-compatible APIs.

## Supported Operations
Every storage connector expects three standard inputs:
- `action`: `upload`, `download`, or `delete`
- `bucket` (or `container`/`space`/`fs`): The storage namespace.
- `key` (or `blob_name`/`file_path`): The exact path or file name.
- `data`: Raw bytes or string required for `upload`.

## Native Cloud Connectors

### Google Cloud Storage (`storage.gcs`)
**Requires:** `google-cloud-storage` (Install with `pip install pyconnectors[gcs]`)
- Config: `credentials_path` (optional, defaults to ambient environment), `project`.

### Azure Blob Storage (`storage.azure_blob`)
**Requires:** `azure-storage-blob` (Install with `pip install pyconnectors[azure_blob]`)
- Config: `connection_string`

### Azure Data Lake Gen2 (`storage.adls`)
**Requires:** `azure-storage-file-datalake` (Install with `pip install pyconnectors[adls]`)
- Config: `connection_string`

### Cloudinary (`storage.cloudinary`)
**Requires:** `cloudinary` (Install with `pip install pyconnectors[cloudinary]`)
- Config: `cloud_name`, `api_key`, `api_secret`
- *Note:* `bucket` is ignored, `file_path` is a local system path for `upload`, and `public_id` is required for `delete`.

## S3 Compatible Connectors

These utilize the lightweight `boto3` client to interact with any S3 API provider.
**Requires:** `boto3` (Install with `pip install pyconnectors[s3]`)

### Amazon S3 (`storage.s3`)
- Config: `aws_access_key_id`, `aws_secret_access_key`, `region_name`

### DigitalOcean Spaces (`storage.digitalocean`)
- Config: `aws_access_key_id`, `aws_secret_access_key`, `region_name` (e.g., `nyc3`)
- Uses `https://[region].digitaloceanspaces.com` automatically.

### Hetzner (`storage.hetzner`)
- Config: `aws_access_key_id`, `aws_secret_access_key`, `region_name` (e.g., `fsn1`)
- Uses `https://[region].your-objectstorage.com` automatically.

### OVHcloud (`storage.ovh`)
- Config: `aws_access_key_id`, `aws_secret_access_key`, `region_name` (e.g., `sbg`)
- Uses `https://s3.[region].perf.cloud.ovh.net` automatically.

### MinIO (`storage.minio`)
- Config: `aws_access_key_id`, `aws_secret_access_key`, `endpoint_url` (Custom explicit host URL).

---

### Example Usage
```python
config = ConnectorConfig(
    params={
        "aws_access_key_id": "DO...",
        "aws_secret_access_key": "sec...",
        "region_name": "nyc3"
    }
)

do = ConnectorFactory.create("storage.digitalocean", config=config)

# Upload
do.execute("upload", "my_space", "document.pdf", data=b"%PDF...")

# Download
result = do.execute("download", "my_space", "document.pdf")
file_bytes = result["data"]
```
