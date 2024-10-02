import pandas as pd
from data_manager import DataManager
from cleaner import Cleaner
from analyzer import Analyzer
import visualizer


def main():
    data = pd.read_csv('student_scores_random_names.csv')

    datamanager = DataManager(data)
    # datamanager.print_data()

    df = datamanager.df
    cleaner = Cleaner(df)

    # cleaner.clean_with_dropna() # Uncomment this line to clean the data with dropna
    # cleaner.clean_with_mean()  # Uncomment this line to clean the data with mean
    cleaner.clean_with_zeros()

    datamanager.save_data_to_file("cleaned_student_scores_random_names.csv")

    analyzer = Analyzer(df)
    print("################## TASK 1 ################################")
    print("Students who failed:")
    print(analyzer.students_who_failed())

    print("################## TASK 2 ################################")
    print("Average scores of the students in each semester:")
    print(analyzer.find_average())

    print("################## TASK 3 ################################")
    print(analyzer.find_students_with_max_avg())

    print("################## TASK 4 ################################")
    print("Subject with the lowest average score and the average score:")
    print(analyzer.lowest_scores())

    print("################## TASK 5 ################################")
    print("New DataFrame with the average scores of the students in each semester:")
    analyzer.new_dataframe()
    data = pd.read_excel('semester_average.xlsx', index_col=0)
    print(data)

    print("################## TASK 6 ################################")
    print("Students who got better:")
    analyzer.students_who_got_better()

    subject_data = analyzer.average_all_subject()
    visualizer.plot_average(subject_data)

    semester_data = analyzer.average_all_semester()
    visualizer.plot_average_semester(semester_data)


if __name__ == '__main__':
    main()