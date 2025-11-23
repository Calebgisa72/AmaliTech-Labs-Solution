class Student:
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

    @classmethod
    def generate_id(cls):
        sid = cls._next_id
        cls._next_id += 1
        return sid


class GraduateStudent(Student):
    def __init__(self, thesis_topic, name):
        super().__init__(name)
        self.thesis_topic = thesis_topic


class UndergraduateStudent(Student):
    pass
