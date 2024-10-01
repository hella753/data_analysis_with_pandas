import pandas as pd
from data_manager import DataManager
from cleaner import Cleaner

def main():
    data = pd.read_csv('student_scores_random_names.csv')

    datamanager = DataManager(data)
    datamanager.print_data()

    df = datamanager.df
    cleaner = Cleaner(df)

    # cleaner.clean_with_mean()  # Uncomment this line to clean the data with mean
    cleaner.clean_with_dropna()

    datamanager.print_data()
    datamanager.save_data_to_file("cleaned_student_scores_random_names")


if __name__ == '__main__':
    main()