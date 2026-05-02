import os
from azure.storage.blob import BlobServiceClient  # type: ignore[import]

CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER", "documents")

def upload_file(filename: str, file_bytes: bytes) -> str:
    """Upload file to Azure Blob Storage and return blob URL."""
    try:
        client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = client.get_container_client(CONTAINER_NAME)

        # Create container if it doesn't exist
        if not container_client.exists():
            container_client.create_container()

        # Upload the file
        blob_client = container_client.get_blob_client(filename)
        blob_client.upload_blob(file_bytes, overwrite=True)

        return blob_client.url

    except Exception as e:
        print(f"Blob upload error: {e}")
        # Return a placeholder if blob storage not configured
        return f"local://{filename}"
