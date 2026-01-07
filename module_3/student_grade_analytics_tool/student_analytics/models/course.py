from dataclasses import dataclass
from typing import Union

Grade = Union[float, int]


@dataclass
class Course:
    course_name: str
    credits: int
    grade: Grade
