from azure.storage.blob import BlobServiceClient

storage_account_key = "JtK+TQyWuDk8PdtEM5U2ht16UlTRcXMZna9O2GvwxFM58Yyl5raOX97hUw1VilQTjulgVXtb73Z5+AStILJ+4A=="
storage_account_name = "mlstocks"
connection_string = "DefaultEndpointsProtocol=https;AccountName=mlstocks;AccountKey=VhtjaKkYjZi0akKct1MrXgH0Vt/SbrYO/STphKlzYhp5zdvFNm3scKBFOAkGNMuIoel1Emm0zvJl+ASt/LplXQ==;EndpointSuffix=core.windows.net"
container_name = "stocks"

def uploadToBlobStorage(file_path, file_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)

    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"Uploaded {file_name}.")

# wrap this in a try except block to catch blob_name errors
def downloadFromBlobStorage(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    blob_data = blob_client.download_blob()
    data = blob_data.readall()
    return data