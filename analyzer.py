from pandas import DataFrame, Series


class Analyzer:
    """
    Responsible for analyzing the data and providing
    basic statistics about the students.
    """
    def __init__(self, dataframe: DataFrame) -> None:
        """
        Initializes the Analyzer object with the given dataframe.

        :param dataframe: DataFrame: DataFrame object containing
        the data of the students.
        """
        self.df = dataframe
        self.numeric_columns: list = self.df.select_dtypes(
            include=['int64', 'float64']
        ).columns.tolist()

    def students_who_failed(self) -> Series:
        """
        Returns the list of students who have failed in at least one subject.

        :return: Series: DataFrame object containing the list of students.
        """
        df = self.df[
            (
                (self.df[self.numeric_columns] < 50) &
                (self.df[self.numeric_columns] > 0)
            ).any(axis=1)]["Student"]
        df = df.drop_duplicates(inplace=False)
        df.reset_index(drop=True, inplace=True)
        return df

    def find_average(self) -> DataFrame:
        """
        Returns the average scores of the students in each semester.

        :return: DataFrame: DataFrame object containing the average scores.
        """
        return self.df.groupby(["Semester"]).mean(numeric_only=True)

    def find_students_with_max_avg(self) -> Series:
        """
        Returns the students with the highest average grade.

        :return: Series: Series object containing the students
        with the highest average grade.
        """
        data = self.df.groupby('Student').agg(
            {
                "Math": ["sum", "count"],
                "Physics": ["sum", "count"],
                "Chemistry": ["sum", "count"],
                "Biology": ["sum", "count"],
                "English": ["sum", "count"]
            }
        )
        student_average_grade: Series = (
                data.xs('sum', axis=1, level=1).sum(axis=1) /   # type: ignore
                data.xs('count', axis=1, level=1).sum(axis=1)   # type: ignore
        )
        max_average = student_average_grade.max()
        students_with_max_avg_grade = (
            student_average_grade[student_average_grade == max_average]
        )
        return students_with_max_avg_grade

    def lowest_scores(self) -> tuple:
        """
        Returns the subject with the lowest average score and
        the average score.

        :return: Tuple: Tuple containing the subject and the average score.
        """
        mean = self.df.mean(numeric_only=True)
        min_value = round(float(mean.min()), 2)
        min_subject = mean.idxmin()
        return min_subject, min_value

    def new_dataframe(self) -> None:
        """
        Creates a new DataFrame with the average scores of the students
        in each semester and saves it to an Excel file.
        """
        semester_average = self.find_average()
        new_df = DataFrame(semester_average)
        new_df.index.name = "Semester"
        new_df.to_excel("data/semester_average.xlsx", index=True)

    @staticmethod
    def comparison(grades: list) -> bool:
        """
        Compares the list to a sorted version of the list and returns True
        if the list is sorted.

        :param grades: list: list containing the average score.
        :return: bool: True if the list is sorted, False otherwise.
        """
        sorted_values: list = sorted(grades)
        if len(grades) <= 1:
            return False
        return list(grades) == sorted_values

    def students_who_got_better(self) -> None:
        """
        Groups the dataframe by student and semester, calculates
        the average score and for each student checks if the average
        cscore got better throughout the semesters
        with the help of the comparison method.
        """
        grouped = self.df.groupby(["Student", "Semester"]).first()
        grouped_average = grouped.mean(axis=1)

        student_improved = grouped_average.groupby(level=0).filter(
            lambda x: self.comparison(x.values)
        )
        students = list(student_improved.index)
        student_names = [student[0] for student in students]
        unique_students = set(student_names)

        for student in unique_students:
            print(student)

    def average_all_subject(self) -> tuple:
        """
        Returns the average scores of all subjects.

        :return: Tuple: Tuple containing the subjects and the average scores.
        """
        data = self.df[self.numeric_columns].mean().round(2)
        columns = list(data.index)
        values = list(data.values)
        return columns, values

    def average_all_semester(self) -> tuple:
        """
        Returns the average scores of all semesters.

        :return: Tuple: Tuple containing the semesters and the average scores.
        """
        data = self.df.groupby("Semester")[self.numeric_columns].agg({
            "Math": ["sum", "count"],
            "Physics": ["sum", "count"],
            "Chemistry": ["sum", "count"],
            "Biology": ["sum", "count"],
            "English": ["sum", "count"]
        })
        average_data: Series = (
            data.xs('sum', axis=1, level=1).sum(axis=1) /   # type: ignore
            data.xs('count', axis=1, level=1).sum(axis=1)   # type: ignore
        )
        x = list(average_data.index)
        y = average_data.to_list()
        return x, y
