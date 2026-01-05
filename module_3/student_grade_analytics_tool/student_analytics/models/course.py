from dataclasses import dataclass
from typing import Union

Grade = Union[float, int]


@dataclass
class Course:
    """
    Represents a course enrollment.

    Attributes:
        course_name (str): Name of the course.
        credits (int): Number of credits.
        grade (Grade): Grade received.
    """

    course_name: str
    credits: int
    grade: Grade
