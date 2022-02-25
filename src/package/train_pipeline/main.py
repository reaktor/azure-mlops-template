import os

import joblib
from azureml.core import Datastore, Dataset
from azureml.core.run import Run
from azureml.core.model import Model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

from package.train_pipeline.constants import (
    TrainPipelineConstants
)

from package.data_pipeline.constants import (
    DataPipelineConstants
)

from package.train_pipeline.transformer import (
    DataTransformer
)


__here__ = os.path.dirname(__file__)


def get_df_from_datastore_path(datastore, datastore_path):
    
    datastore_path = [(datastore, datastore_path)]

    dataset = Dataset.Tabular.from_delimited_files(
        path=datastore_path
    )

    dataframe = dataset.to_pandas_dataframe()

    return dataframe


def prepare_data(workspace):

    print("Loading training datastore:", DataPipelineConstants.TRAINING_DATASTORE.value)
    datastore_train = Datastore.get(
        workspace, DataPipelineConstants.TRAINING_DATASTORE.value)

    print("Loading evaluation datastore:", DataPipelineConstants.EVALUATION_DATASTORE.value)
    datastore_test = Datastore.get(
        workspace, DataPipelineConstants.EVALUATION_DATASTORE.value)

    print("Loading validation datastore:", DataPipelineConstants.VALIDATION_DATASTORE.value)
    datastore_validation = Datastore.get(
        workspace, DataPipelineConstants.VALIDATION_DATASTORE.value)

    # Load data
    print("Loading training data")
    x_train = get_df_from_datastore_path(datastore_train, 'X_train.csv')
    y_train = get_df_from_datastore_path(datastore_train, 'y_train.csv')
    y_train = y_train['Target']

    print("Loading evaluation data")
    x_test = get_df_from_datastore_path(datastore_test, 'X_test.csv')
    y_test = get_df_from_datastore_path(datastore_test, 'y_test.csv')
    y_test = y_test['Target']

    print("Loading validation data")
    x_valid = get_df_from_datastore_path(datastore_validation, 'X_valid.csv')
    y_valid = get_df_from_datastore_path(datastore_validation, 'y_valid.csv')
    y_valid = y_valid['Target']

    # Transform data
    x_train = DataTransformer.some_transformation(x_train)
    x_train = DataTransformer.some_other_transformation(x_train)

    x_test = DataTransformer.some_transformation(x_test)
    x_test = DataTransformer.some_other_transformation(x_test)

    x_valid = DataTransformer.some_transformation(x_valid)
    x_valid = DataTransformer.some_other_transformation(x_valid)

    return x_train, y_train, x_test, y_test, x_valid, y_valid


def train_model(x_train, y_train):

    classifier = LogisticRegression()

    classifier.fit(x_train, y_train)

    return classifier


def evaluate_model(classifier, x_test, y_test):

    y_pred = classifier.predict(x_test)

    model_f1_score = f1_score(y_test, y_pred)

    print("F1 score:", model_f1_score)

def save_model(classifer):

    output_dir = os.path.join(__here__, 'outputs')
    os.makedirs(output_dir, exist_ok=True)

    model_path = os.path.join(output_dir, 'model.pkl')
    joblib.dump(classifer, model_path)

    return model_path


def register_model(ws, model_path):

    print("Starting to register model")
    model = Model.register(
        workspace = ws,
        model_name=TrainPipelineConstants.MODEL_NAME.value,
        model_path=model_path
    )

    print("Registered model")

from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core import Workspace, Datastore, Dataset, Model

def main():

    tenant_id = os.environ['TENANT_ID']
    service_principal_id = os.environ['SERVICE_PRINCIPAL_ID']
    service_principal_password = os.environ['SERVICE_PRINCIPAL_PASSWORD']
    workspace_name = os.environ['WORKSPACE_NAME']
    resource_group = os.environ['RESOURCE_GROUP_NAME']
    subscription_id = os.environ['SUBSCRIPTION_ID']

    # Auth
    auth = ServicePrincipalAuthentication(
        tenant_id,
        service_principal_id,
        service_principal_password)

    # Workspace
    workspace = Workspace(
        subscription_id = subscription_id,
        resource_group = resource_group,
        workspace_name = workspace_name,
        auth=auth)

    #run = Run.get_context()
    #workspace = run.experiment.workspace
    
    x_train, y_train, x_test, y_test, x_valid, y_valid = prepare_data(workspace)

    print(x_train)

    classifier = train_model(x_train, y_train)

    evaluate_model(classifier, x_test, y_test)

    model_path = save_model(classifier)

    register_model(workspace, model_path)


if __name__ == '__main__':
    main()
