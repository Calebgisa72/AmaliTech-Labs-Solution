from dataclasses import dataclass, field
from typing import List
from .course import Course


@dataclass
class Student:
    student_id: str
    name: str
    major: str
    year: int
    courses: List[Course] = field(default_factory=list)
