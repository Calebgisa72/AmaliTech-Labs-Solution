from .student import Student
from .course import Course


class Enrollment:
    def __init__(self):
        self.records = {}

    def enroll(self, student: Student, course: Course):
        self.records.setdefault(student.student_id, []).append(course)

    def get_student_courses(self, student_id):
        return self.records.get(student_id, [])

    def is_enrolled(self, student_id, course: Course):
        return course in self.records.get(student_id, [])

    def print_records(self):
        if not self.records:
            print("\nThe system has no enrollments for now.")
            return
        for student_id, courses in self.records.items():
            print(f"\nStudent {student_id} is enrolled in:")
            for c in courses:
                print(f"   - {c.title}")
