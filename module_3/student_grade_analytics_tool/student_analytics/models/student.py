from dataclasses import dataclass, field
from typing import List
from .course import Course


@dataclass
class Student:
    """
    Represents a student.

    Attributes:
        student_id (str): Unique identifier.
        name (str): Full name.
        courses (List[Course]): List of enrolled courses.
    """

    student_id: str
    name: str
    courses: List[Course] = field(default_factory=list)
