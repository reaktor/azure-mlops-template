# pylint: skip-file
import json

import joblib
import numpy as np
from azureml.core.model import Model

from package.train_pipeline.constants import (
    TrainPipelineConstants
)


def init():

    global model

    model_path = Model.get_model_path(TrainPipelineConstants.MODEL_NAME.value)
    model = joblib.load(model_path)


def run(data):
    
    try:
        data = json.loads(data)
        data = data['data']
        result = model.predict(np.array(data))
        return result.tolist()
    except Exception as e:
        error = str(e)
        return error
