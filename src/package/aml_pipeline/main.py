import os

from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.environment import Environment

from package.interfaces.aml import (
    AMLInterface
)

from package.aml_pipeline.constants import (
    AMLPipelineConstants
)


def get_dist_dir():
    path = os.path.dirname(__file__)
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    dist_dir = os.path.join(path, 'dist')
    return dist_dir


def retrieve_whl_filepath():

    dist_dir = get_dist_dir()
    if not os.path.isdir(dist_dir):
        raise FileNotFoundError("Couldn't find dist directory")

    dist_files = os.listdir(dist_dir)
    print(dist_files)
    whl_file = [
        f for f in dist_files
        if f.startswith('my_ml_project')
        and f.endswith('whl')
    ]

    if not whl_file:
        raise FileNotFoundError("Couldn't find wheel file")

    return os.path.join(dist_dir, whl_file[0])


def create_aml_environment(aml_interface):
    """
    Creates the Azure Machine Learning Environment.
    """
    aml_env = Environment(
        name=AMLPipelineConstants.AML_ENV_NAME.value)
    conda_dep = CondaDependencies()
    conda_dep.add_pip_package("numpy==1.18.2")
    conda_dep.add_pip_package("pandas==1.0.3")
    conda_dep.add_pip_package("scikit-learn==0.22.2.post1")
    conda_dep.add_pip_package("joblib==0.14.1")
    whl_filepath = retrieve_whl_filepath()
    whl_url = Environment.add_private_pip_wheel(
        workspace=aml_interface.workspace,
        file_path=whl_filepath,
        exist_ok=True
    )
    conda_dep.add_pip_package(whl_url)
    aml_env.python.conda_dependencies = conda_dep
    aml_env.docker.enabled = True
    return aml_env


def main():
    
    workspace_name = os.environ['WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP_NAME']
    subscription_id = os.environ['SUBSCRIPTION_ID']

    print("workspace_name:", workspace_name)
    print("resource_group:", resource_group)

    service_principal_credentials = {
        'tenant_id': os.environ['TENANT_ID'],
        'service_principal_id': os.environ['SERVICE_PRINCIPAL_ID'],
        'service_principal_password': os.environ['SERVICE_PRINCIPAL_PASSWORD'],
    }

    aml_interface = AMLInterface(
        service_principal_credentials,
         subscription_id, workspace_name, resource_group
    )

    aml_env = create_aml_environment(aml_interface)
    aml_interface.register_aml_environment(aml_env)


if __name__ == '__main__':
    main()