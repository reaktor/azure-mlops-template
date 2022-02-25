

class DataTransformer:
    """
    Implements data transformations.
    """

    @staticmethod
    def some_transformation(data):
        """
        Implements some transformation
        """
        return data.drop(['D', 'I'], axis=1)


    @staticmethod
    def some_other_transformation(data):
        """
        Implements some other clever transformation
        """
        return 1.5 * data
