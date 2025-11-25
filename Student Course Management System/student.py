from abc import ABC, abstractmethod
from typing import Any

class Student(ABC):
    _next_id = 1

    def __init__(self, name):
        self.student_id = Student.generate_id()
        self.name = name

        if isinstance(self, GraduateStudent):
            self.level = "Graduate"
        elif isinstance(self, UndergraduateStudent):
            self.level = "Undergraduate"

    def __str__(self):
        return f"{self.student_id} - {self.name} ({self.level})"
    
    @abstractmethod
    def get_student_details(self) -> dict[str, Any]:
        pass

    @classmethod
    def generate_id(cls):
        sid = cls._next_id
        cls._next_id += 1
        return sid


class GraduateStudent(Student):
    def __init__(self, thesis_topic, name):
        super().__init__(name)
        self.thesis_topic = thesis_topic
    
    def get_student_details(self) -> dict[str, Any]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "level": self.level,
            "thesis_topic": self.thesis_topic
        }


class UndergraduateStudent(Student):
    def __init__(self, name):
        super().__init__(name)
    def get_student_details(self) -> dict[str, Any]:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "level": self.level
        }