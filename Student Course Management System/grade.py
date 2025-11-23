from data_store import courses, students

class Grade:
    def __init__(self):
        self.grades = {}

    def add_student_marks(self, student_id, course_code, marks: float):
        self.grades.setdefault(student_id, {})[course_code] = marks

    def get_students_marks(self, student_id):
        if not self.grades:
            print("\nThe system has no marks for now.")
            return

        student = students[student_id]
        student_marks = self.grades.get(student_id, {})

        if not student_marks:
            print(f"\nNo marks found for {student.name}.")
            return

        total = 0
        print(f"\nMarks for {student.name}:")

        for course_code, marks in student_marks.items():
            course_title = courses[course_code].title
            total += marks
            print(f"   - {course_title}: {marks}")

        avg = total / len(student_marks)
        print(f"\nStudent's Average = {avg:.2f}")

    def get_course_student_marks(self, course_code):
        if not self.grades:
            print("\nThe system has no marks for now.")
            return

        course_title = courses[course_code].title
        print(f"\nMarks for {course_title}:")

        found = False
        for sid, marks_dict in self.grades.items():
            if course_code in marks_dict:
                found = True
                student_name = students[sid].name
                print(f"   - {student_name}: {marks_dict[course_code]}")

        if not found:
            print("No marks found for this course.")
