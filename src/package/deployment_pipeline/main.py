import os

from azureml.core.environment import Environment
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import AciWebservice, Webservice

from package.interfaces.aml import (
    AMLInterface
)

from package.aml_pipeline.constants import (
    AMLPipelineConstants
)

from package.train_pipeline.constants import (
    TrainPipelineConstants
)

from package.deployment_pipeline.constants import (
    DeploymentPipelineConstants
)


__here__ = os.path.dirname(__file__)


def get_inference_config(aml_interface):
    """
    Defines inference configuration
    """
    aml_env = Environment.get(
        workspace=aml_interface.workspace,
        name=AMLPipelineConstants.AML_ENV_NAME.value
    )

    inference_script_path = os.path.join(__here__, 'inference.py')

    config = InferenceConfig(
        entry_script=inference_script_path,
        environment=aml_env
    )

    return config


def get_deployment_config():
    """
    Defines deployment configuration
    """
    config = AciWebservice.deploy_configuration(
        cpu_cores = DeploymentPipelineConstants.CPU_CORES.value,
        memory_gb = DeploymentPipelineConstants.MEMORY_SIZE_GB.value
    )

    return config


def deploy_service(aml_interface):  
    """
    Deploy the inference service
    """

    inference_config = get_inference_config(aml_interface)

    deployment_config = get_deployment_config()
    
    model = aml_interface.workspace.models.get(
        TrainPipelineConstants.MODEL_NAME.value
    )

    service = Model.deploy(
        aml_interface.workspace,
        DeploymentPipelineConstants.DEPLOYMENT_SERVICE_NAME.value,
        [model],
        inference_config,
        deployment_config,
        overwrite=True
    )

    service.wait_for_deployment(show_output=True)
    print(service.get_logs())
    print(service.scoring_uri)


def update_service(aml_interface):

    inference_config = get_inference_config(aml_interface)
    service = Webservice(
        name=DeploymentPipelineConstants.DEPLOYMENT_SERVICE_NAME.value,
        workspace=aml_interface.workspace
    )

    model = aml_interface.workspace.models.get(TrainPipelineConstants.MODEL_NAME.value)
    service.update(models=[model], inference_config=inference_config)

    print(service.state)
    print(service.scoring_uri)


def main():

    subscription_id = os.environ['SUBSCRIPTION_ID']
    workspace_name = os.environ['WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP_NAME']
    
    service_principal_credentials = {
        'tenant_id': os.environ['TENANT_ID'],
        'service_principal_id': os.environ['SERVICE_PRINCIPAL_ID'],
        'service_principal_password': os.environ['SERVICE_PRINCIPAL_PASSWORD'],
    }

    aml_interface = AMLInterface(
        service_principal_credentials, subscription_id, workspace_name, resource_group
    )

    webservices = aml_interface.workspace.webservices.keys()
    if DeploymentPipelineConstants.DEPLOYMENT_SERVICE_NAME.value not in webservices:
        deploy_service(aml_interface)
    else:
        update_service(aml_interface)


if __name__ == '__main__':
    main()
