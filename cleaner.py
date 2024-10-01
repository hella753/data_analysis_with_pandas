from pandas import DataFrame


class Cleaner:
    """
    Class for Data Cleaning, fixing empty cells and duplicates
    """
    def __init__(self, dataframe: DataFrame):
        """
        Creates the Cleaner object

        :param dataframe: DataFrame: pandas dataframe object
        """
        self.df: DataFrame = dataframe
        self.df.drop_duplicates(inplace=True)

    def clean_with_dropna(self) -> DataFrame:
        """
        Removes rows with empty cells

        :return: DataFrame: cleaned dataframe
        """
        self.df.dropna(inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        return self.df

    def clean_with_mean(self) -> DataFrame:
        """
        Fills empty cells with the mean of the column

        :return: DataFrame: cleaned dataframe
        """
        mean = round(self.df.mean(numeric_only=True))
        self.df.fillna(
            {
                'Math': mean["Math"],
                'Physics': mean["Physics"],
                'Chemistry': mean["Chemistry"],
                'Biology': mean['Biology'],
                'English': mean['English']
            },
            inplace=True
        )
        return self.df
