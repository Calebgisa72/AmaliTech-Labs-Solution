from ..models.student import Student
from typing import List, Union
from collections import Counter, defaultdict, OrderedDict


class AnalysisService:
    """
    Service for performing statistical analysis on student data.
    """

    @staticmethod
    def calculate_distribution(grades: List[Union[float, int]]) -> Counter:
        """
        Calculates the distribution of grades.

        Using Counter for efficient counting.
        """
        return Counter(grades)

    @staticmethod
    def group_by_major(students: List[Student]) -> defaultdict:
        """
        Groups students by their major.

        Using defaultdict for automatic list initialization.
        """
        grouped = defaultdict(list)
        for student in students:
            grouped[student.major].append(student)
        return grouped

    @staticmethod
    def overall_statistics(students: List[Student]) -> OrderedDict:
        """
        Calculates overall statistics for a list of students.
        """
        all_grades = [
            course.grade
            for student in students
            for course in student.courses
            if isinstance(course.grade, (int, float))
        ]

        if not all_grades:
            return OrderedDict([("mean", 0.0), ("median", 0.0), ("mode", 0.0)])

        import statistics

        stats: OrderedDict[str, Union[float, str]] = OrderedDict()
        stats["mean"] = round(statistics.mean(all_grades), 2)
        stats["median"] = round(statistics.median(all_grades), 2)
        try:
            stats["mode"] = round(statistics.mode(all_grades), 2)
        except statistics.StatisticsError:
            stats["mode"] = "Multimodal"

        return stats
