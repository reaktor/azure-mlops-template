import os

from package.interfaces.blob import (
    BlobStorageInterface
)

from package.interfaces.aml import (
    AMLInterface
)

from package.data_pipeline.job import (
    DataPipelineJob
)

from package.data_pipeline.constants import (
    DataPipelineConstants
)

def main():

    storage_account_name = os.environ['STORAGE_ACCOUNT_NAME']
    storage_account_key = os.environ['STORAGE_ACCOUNT_KEY']

    print('STORAGE_ACCOUNT_NAME:', storage_account_name)
    print('STORAGE_ACCOUNT_KEY:', storage_account_key)

    storage_interface = BlobStorageInterface(
        storage_account_name, storage_account_key
    )

    # Create new datasets for the train pipeline and upload them
    # to the blob storage.
    data_pipeline_job = DataPipelineJob()
    data_pipeline_job.create()
    data_pipeline_job.upload_data(storage_interface)

    subscription_id = os.environ['SUBSCRIPTION_ID']
    workspace_name = os.environ['WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP_NAME']
    
    service_principal_credentials = {
        'tenant_id': os.environ['TENANT_ID'],
        'service_principal_id': os.environ['SERVICE_PRINCIPAL_ID'],
        'service_principal_password': os.environ['SERVICE_PRINCIPAL_PASSWORD'],
    }

    aml_interface = AMLInterface(
        service_principal_credentials, subscription_id,
        workspace_name, resource_group
    )

    # Register the blob storage as a datastore for the aml workspace.
    aml_interface.register_datastore(
        DataPipelineConstants.TRAINING_DATASTORE.value, 
        DataPipelineConstants.TRAINING_CONTAINER.value,
        storage_account_name, storage_account_key
    )
    aml_interface.register_datastore(
        DataPipelineConstants.VALIDATION_DATASTORE.value, 
        DataPipelineConstants.VALIDATION_CONTAINER.value,
        storage_account_name, storage_account_key
    )
    aml_interface.register_datastore(
        DataPipelineConstants.EVALUATION_DATASTORE.value, 
        DataPipelineConstants.EVALUATION_CONTAINER.value,
        storage_account_name, storage_account_key
    )


if __name__ == '__main__':
    main()
