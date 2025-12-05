from data_store import students, courses
from models.student import GraduateStudent, UndergraduateStudent
from models.course import Course
from utils import get_int, get_float, get_non_empty_string


def choose_level(label: str) -> int | None:
    while True:
        print(f"\nEnter {label} level:")
        print("1. Undergraduate")
        print("2. Graduate")

        level_choice = get_int("Choose an option (or 'q' to quit): ")

        if level_choice is None:
            return None

        if level_choice in (1, 2):
            return level_choice

        print("Invalid choice!")


def show_all_student_ids():
    print("\nAvailable Students:")
    if not students:
        print("  (none)")
        return
    for student in students.values():
        print(student)


def get_student_courses(student_id: int):
    student = students[student_id]
    filtered = [c for c in courses.values() if c.level == student.level]

    if not filtered:
        print(f"\nNo courses available for level: {student.level}")
        return None
    return filtered


def add_student():
    level = choose_level("student")
    if level is None:
        return

    if level == 2:
        topic = get_non_empty_string("\nEnter thesis topic (or 'q' to quit): ")
        if topic is None:
            return

        name = get_non_empty_string("Enter student name: ")
        if name is None:
            return

        student = GraduateStudent(topic, name)

    else:
        name = get_non_empty_string("Enter student name: ")
        if name is None:
            return

        student = UndergraduateStudent(name)

    students[student.student_id] = student
    print(f"Student added successfully! Assigned ID = {student.student_id}")


def add_course():
    level = choose_level("course")
    if level is None:
        return

    code = get_non_empty_string("\nEnter course code: ")
    if code is None:
        return
    code = code.upper()

    title = get_non_empty_string("Enter course title: ")
    if title is None:
        return

    level_name = "Undergraduate" if level == 1 else "Graduate"

    courses[code] = Course(code, title, level_name)
    print("Course added successfully!")


def enroll_student(enrollment):
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")
    if sid is None:
        return

    if sid not in students:
        print("Student not found!")
        return

    available = get_student_courses(sid)
    if not available:
        return

    already_enrolled = enrollment.get_student_courses(sid)
    available = [c for c in available if c not in already_enrolled]

    if not available:
        print("\nStudent is already enrolled in all available courses for this level.")
        return

    print("\nAvailable courses:")
    for c in available:
        print(f" - {c.code}: {c.title}")

    code = get_non_empty_string("Enter course code to enroll: ")
    if code is None:
        return
    code = code.upper()

    if code not in courses:
        print("Course not found!")
        return

    if courses[code] not in available:
        print("This student is already enrolled in that course.")
        return

    enrollment.enroll(students[sid], courses[code])
    print("Enrollment successful!")



def assign_grade(enrollment, grade):
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")
    if sid is None:
        return

    if sid not in students:
        print("Student not found!")
        return

    available = get_student_courses(sid)
    if not available:
        return

    print("\nAvailable courses:")
    for c in available:
        print(f" - {c.code}: {c.title}")

    code = get_non_empty_string("Enter course code: ")
    if code is None:
        return
    code = code.upper()

    if (
        sid not in enrollment.records
        or code not in courses
        or enrollment.is_enrolled(sid, courses[code]) is False
    ):
        print("First enroll this student in this course!")
        return

    marks = get_float("Enter student marks: ")
    if marks is None:
        return

    grade.add_student_marks(sid, code, marks)
    print("Marks added successfully!")


def show_student_marks(grade):
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")
    if sid is None:
        return

    grade.get_students_marks(sid)


def show_course_marks(grade):
    code = get_non_empty_string("\nEnter course code: ")
    if code is None:
        return

    code = code.upper()

    if code not in courses:
        print("Course not found!")
        return

    grade.get_course_student_marks(code)


def list_students():
    if not students:
        print("No students found.")
        return

    print("\n--- All Students ---")
    for s in students.values():
        print(f" {s}")


def list_courses():
    if not courses:
        print("No courses found.")
        return

    print("\n--- All Courses ---")
    for c in courses.values():
        print(f" - {c}")


def get_student_details():
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")
    if sid is None:
        return

    if sid not in students:
        print("Student not found!")
        return

    details = students[sid].get_student_details()

    print("\n--- Student Details ---")
    for k, v in details.items():
        print(f"{k.capitalize()}: {v}")
