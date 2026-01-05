from typing import List, Dict, Any
from ..models.student import Student
from .analysis_service import AnalysisService


class ReportService:
    """
    Service for generating formatted reports from student analysis.
    """

    @staticmethod
    def generate_report(students: List[Student]) -> Dict[str, Any]:
        """
        Generates a comprehensive analysis report.

        Args:
            students (List[Student]): List of Student objects.

        Returns:
            Dict[str, Any]: Structured report dictionary.
        """
        if not students:
            return {"error": "No student data available"}

        # 1. Overall Statistics
        overall_stats = AnalysisService.overall_statistics(students)

        # 2. Grade Distribution (Rounded)
        all_grades = [
            course.grade
            for student in students
            for course in student.courses
            if isinstance(course.grade, (int, float))
        ]
        from typing import Union

        # Round grades to nearest integer for meaningful distribution
        # Explicit annotation to satisfy List invariance (List[int] is not List[Union[float, int]])
        rounded_grades: List[Union[float, int]] = [int(round(g)) for g in all_grades]
        distribution = AnalysisService.calculate_distribution(rounded_grades)

        # 3. Group by Major (Count only for report summary)
        grouped_by_major = AnalysisService.group_by_major(students)
        major_counts = {
            major: len(st_list) for major, st_list in grouped_by_major.items()
        }

        # 4. Top Students
        # Calculate average per student
        student_averages: List[Dict[str, Any]] = []
        for student in students:
            valid_grades = [
                c.grade for c in student.courses if isinstance(c.grade, (int, float))
            ]
            avg = sum(valid_grades) / len(valid_grades) if valid_grades else 0.0
            student_averages.append(
                {
                    "student_id": student.student_id,
                    "name": student.name,
                    "average_grade": round(avg, 2),
                }
            )

        # Sort by average grade descending
        # Explicit cast to float to satisfy Mypy
        top_students = sorted(
            student_averages, key=lambda x: float(str(x["average_grade"])), reverse=True
        )[:3]

        report = {
            "overall_statistics": dict(overall_stats),
            "grade_distribution": dict(distribution),
            "major_enrollment": major_counts,
            "top_performers": top_students,
        }

        return report
