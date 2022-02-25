from enum import Enum

class DataPipelineConstants(Enum):

    TRAINING_CONTAINER = 'train'
    VALIDATION_CONTAINER = 'validation'
    EVALUATION_CONTAINER = 'evaluation'

    TRAINING_DATASTORE = 'data_store_train'
    VALIDATION_DATASTORE = 'data_store_validation'
    EVALUATION_DATASTORE = 'data_store_evaluation'
