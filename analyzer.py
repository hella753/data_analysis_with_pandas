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
        print(data)
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
    def comparison(stud_dict: dict) -> str:
        """
        Compares the values of the dictionary and returns the key
        of the dictionary if the values are sorted in ascending
        order naturally.

        :param stud_dict: dict: Dictionary containing the student,
        semester and the average score.
        :return: str: The student who's average score got better
        throughout the semesters.
        """
        values_list: list = list(stud_dict.values())
        sorted_values: list = sorted(values_list)
        # print(values_list)
        if sorted_values == values_list and values_list:
            student_name = list(stud_dict.keys())[0]
            # print(sorted_values, values_list)
            return student_name

    def students_who_got_better(self) -> None:
        """
        Groups the dataframe by student and semester, calculates
        the average score and for each student checks if the average
        score got better throughout the semesters
        with the help of the comparison method.
        """
        grouped = self.df.groupby(["Student", "Semester"]).first()
        grouped_average = grouped.mean(axis=1)

        # For tracking changes
        previous_student = None
        previous_value = None
        student_dict = {}

        for student, score in grouped_average.items():
            student_name, semester = student

            # For the first student
            if previous_student is None:
                previous_student = student_name
                previous_value = score

            if previous_student != student_name:
                previous_student = student_name
                previous_value = score
                compared = self.comparison(student_dict)
                if compared:
                    print(compared)
                student_dict = {}
            else:
                student_dict[previous_student] = previous_value
                student_dict[student] = score

        # For the last student
        compared = self.comparison(student_dict)
        if compared:
            print(compared)

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
