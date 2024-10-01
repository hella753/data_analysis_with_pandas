import pandas as pd
from pandas import DataFrame, Series
from typing import Any


class DataManager:
    """
    DataManager class to manage the data in the dataframe.
    It provides methods to access, modify and manipulate the data.
    """
    def __init__(self, dataframe: DataFrame) -> None:
        """
        Creates the DataManager object

        :param dataframe: pandas dataframe object
        """
        self.df: DataFrame = dataframe

    def print_data(self) -> None:
        """
        Prints the data in the dataframe
        """
        print(self.df)

    def get_column(self, column_name: str) -> Series:
        """
        Returns the column data

        :param column_name: str: name of the column
        :return: Series: column data
        """
        return self.df[column_name]

    def get_row(self, row_number: int) -> Series:
        """
        Returns the row data

        :param row_number: int: row number
        :return: Series: row data
        """
        return self.df.iloc[row_number]

    def get_value(self, row_number: int, column_name: str) -> Any:
        """
        Returns the value at the specified row and column

        :param row_number: int: row number
        :param column_name: str: column name
        :return: any: value at the specified row and column
        """
        return self.df.at[row_number, column_name]

    def add_column(self, column_name: str, column_data: list) -> None:
        """
        Adds a column to the dataframe

        :param column_name: str: name of the column
        :param column_data: list: data to be added to the column
        :return: None
        """
        self.df[column_name] = column_data

    def remove_column(self, column_name: str) -> None:
        """
        Removes the specified column from the dataframe

        :param column_name: str: name of the column to be removed
        :return: None
        """
        try:
            self.df.drop(column_name, axis=1, inplace=True)
        except KeyError:
            print(f'Column {column_name} not found')

    def add_row(self, row_data: dict) -> None:
        """
        Adds a row to the dataframe

        :param row_data: dict: data to be added to the row
        :return: None
        """
        row_df = DataFrame([row_data])
        self.df = pd.concat([self.df, row_df], ignore_index=True)

    def save_data_to_file(self, file_name: str) -> None:
        """
        Saves the data in the dataframe to a file

        :param file_name: str: name of the file
        """
        self.df.to_csv(f'{file_name}.csv', index=False)