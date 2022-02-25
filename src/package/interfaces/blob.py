from io import StringIO

import pandas as pd

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient


class BlobStorageInterface:

    def __init__(self, storage_acct_name, storage_acct_key):

        conn_str = (
            'DefaultEndpointsProtocol=https;'
            + f'AccountName={storage_acct_name};'
            + f'AccountKey={storage_acct_key};'
            + 'EndpointSuffix=core.windows.net'
        )

        print("ConnectionString:", conn_str)

        self.blob_service_client = BlobServiceClient.from_connection_string(
            conn_str
        )

    def create_container(self, container_name):
        
        print("Trying to create container:", container_name)
        try:
            self.blob_service_client.create_container(container_name)
        except ResourceExistsError as e:
            print("Failed to create container. It probably exists.")
            

    def upload_df_to_blob(self, dataframe, container_name, remote_path):
        
        print("Creating container:", container_name)
        self.create_container(container_name)

        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=remote_path
        )

        try:
            print(dataframe)
            blob_client.upload_blob(
                dataframe.to_csv(index=False, header=True).encode()
            )
        except ResourceExistsError as e:
            print('Could not upload df to blob:', container_name)
            blob_client.delete_blob()
            print('Deleted blob due to the error')
            #blob_client.upload_blob(
            #    dataframe.to_csv(index=False, header=True).encode()
            #)

    def download_blob_to_df(self, container_name, remote_path):

        blob_client = self.blob_service_client.get_blob_client(
            container=container_name,
            blob=remote_path
        )

        stream = blob_client.download_blob()
        buffer = StringIO(stream.content_as_text())
        dataframe = pd.read_csv(buffer)
        
        return dataframe
