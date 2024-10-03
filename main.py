import pandas as pd
from data_manager import DataManager
from cleaner import Cleaner
from analyzer import Analyzer
import visualizer


def main():
    data = pd.read_csv('data/student_scores_random_names.csv')

    datamanager = DataManager(data)
    df = datamanager.print_data()

    # Drops the rows with all NaN values in numeric columns
    cleaner = Cleaner(df)
    datamanager.print_data()

    # Uncomment this line to drop NaN values (NOT RECOMMENDED)
    # cleaner.clean_with_dropna()
    # Uncomment this line to replace NaN values with the mean (NOT RECOMMENDED)
    # cleaner.clean_with_mean()
    # Uncomment this line to replace NaN values with zeros (NOT RECOMMENDED)
    # df = cleaner.clean_with_zeros()
    # datamanager.print_data()

    datamanager.save_to_csv("data/cleaned_student_scores_random_names.csv")

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
    print(
        "New DataFrame with the average scores of the students "
        "in each semester:"
    )
    analyzer.new_dataframe()
    data = pd.read_excel('data/semester_average.xlsx', index_col=0)
    print(data)

    print("################## TASK 6 ################################")
    print("Students who got better:")
    analyzer.students_who_got_better()

    # Get the average of all subjects
    subject_data = analyzer.average_all_subject()

    # Plot the average of all subjects
    visualizer.plot_average(subject_data)

    # Get the average of all semesters
    semester_data = analyzer.average_all_semester()

    # Plot the average of all semesters
    visualizer.plot_average_semester(semester_data)


if __name__ == '__main__':
    main()
