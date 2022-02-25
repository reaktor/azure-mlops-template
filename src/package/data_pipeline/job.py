import pandas as pd

from sklearn.datasets import (
    make_classification
)

from package.interfaces.split import (
    BaseTestTrainSplit
)

from package.data_pipeline.constants import (
    DataPipelineConstants
)


class DataPipelineJob(BaseTestTrainSplit):
    
    def __init__(self):
            BaseTestTrainSplit.__init__(
                self, DataPipelineConstants)
    
    def create(self):
        
        # TODO: replace this with real data
        x_arr, y_arr = make_classification(
            n_samples=5000,
            n_features=10,
            n_classes=2,
            random_state=1
        )

        col_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        x_df = pd.DataFrame(x_arr, columns=col_names)
        y_df = pd.DataFrame({'Target': y_arr})

        # Training set n=3500
        self.x_train = x_df.iloc[:3500]
        self.y_train = y_df.iloc[:3500]

        # Testing set n=750
        self.x_test = x_df.iloc[3500:4250]
        self.y_test = y_df.iloc[3500:4250]

        # Validation set n=750
        self.x_valid = x_df.iloc[4250:]
        self.y_valid = y_df.iloc[4250:]
        