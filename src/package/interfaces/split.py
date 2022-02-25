

class BaseTestTrainSplit:
    
    def __init__(self, constants):
        self.constants = constants
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.x_valid = None
        self.y_valid = None

    def upload_training_data(self, storage):
        
        print(
            "Uploading training data to:", 
            self.constants.TRAINING_CONTAINER.value
        )
        
        storage.upload_df_to_blob(
            self.x_train,
            self.constants.TRAINING_CONTAINER.value,
            'X_train.csv'
        )

        storage.upload_df_to_blob(
            self.y_train,
            self.constants.TRAINING_CONTAINER.value,
            'y_train.csv'
        )

    def upload_evaluation_data(self, storage):
        
        print(
            "Uploading evaluation data to:", 
            self.constants.EVALUATION_CONTAINER.value
        )
        storage.upload_df_to_blob(
            self.x_test,
            self.constants.EVALUATION_CONTAINER.value,
            'X_test.csv'
        )

        storage.upload_df_to_blob(
            self.y_test,
            self.constants.EVALUATION_CONTAINER.value,
            'y_test.csv'
        )

    def upload_validation_data(self, storage):

        print(
            "Uploading scoring data to:",
             self.constants.VALIDATION_CONTAINER.value
        )

        storage.upload_df_to_blob(
            self.x_valid,
            self.constants.VALIDATION_CONTAINER.value,
            'X_valid.csv'
        )

        storage.upload_df_to_blob(
            self.y_valid,
            self.constants.VALIDATION_CONTAINER.value,
            'y_valid.csv'
        )

    def upload_data(self, storage):
        self.upload_training_data(storage)
        self.upload_evaluation_data(storage)
        self.upload_validation_data(storage)