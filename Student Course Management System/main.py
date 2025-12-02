from typing import Iterable
from grade import Grade
from student import GraduateStudent, UndergraduateStudent
from course import Course
from enrollment import Enrollment
from data_store import students, courses
from utils import get_int, get_float, get_non_empty_string


def choose_level(label: str) -> int:
    """Choose undergraduate or graduate level."""
    while True:
        print(f"\nEnter {label} level:")
        print("1. Undergraduate")
        print("2. Graduate")
        level_choice = get_int("Choose an option: ")
        if level_choice in (1, 2):
            return level_choice
        print("Invalid choice!")


def show_all_student_ids():
    """Print a list of all registered students."""
    print("\nAvailable Students:")
    if not students:
        print("  (none)")
        return
    for student in students.values():
        print(student)


def get_student_courses(student_id: int):
    """Return all courses matching a student's level."""
    student = students[student_id]
    filtered = [c for c in courses.values() if c.level == student.level]

    if not filtered:
        print(f"\nNo courses available for level: {student.level}")
        return None
    return filtered


def add_student():
    level = choose_level("student")

    if level == 2:
        topic = get_non_empty_string("\nEnter thesis topic: ")
        name = get_non_empty_string("Enter student name: ")
        student = GraduateStudent(topic, name)
    else:
        name = get_non_empty_string("Enter student name: ")
        student = UndergraduateStudent(name)

    students[student.student_id] = student
    print(f"Student added successfully! Assigned ID = {student.student_id}")


def add_course():
    level = choose_level("course")

    code = get_non_empty_string("\nEnter course code: ").upper()
    title = get_non_empty_string("Enter course title: ")
    level_name = "Undergraduate" if level == 1 else "Graduate"

    courses[code] = Course(code, title, level_name)
    print("Course added successfully!")


def enroll_student(enrollment: Enrollment):
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")

    if sid not in students:
        print("Student not found!")
        return

    available = get_student_courses(sid)
    if not available:
        return

    print("\nAvailable courses:")
    for c in available:
        print(f" - {c.code}: {c.title}")

    code = get_non_empty_string("Enter course code to enroll: ").upper()

    if code not in courses:
        print("Course not found!")
        return

    enrollment.enroll(students[sid], courses[code])
    print("Enrollment successful!")


def assign_grade(enrollment: Enrollment, grade: Grade):
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")

    if sid not in students:
        print("Student not found!")
        return

    available = get_student_courses(sid)
    if not available:
        return

    print("\nAvailable courses:")
    for c in available:
        print(f" - {c.code}: {c.title}")

    code = get_non_empty_string("Enter course code: ").upper()

    if (
        sid not in enrollment.records
        or code not in courses
        or courses[code] not in enrollment.records[sid]
    ):
        print("First enroll this student in this course!")
        return

    marks = get_float("Enter student marks: ")
    grade.add_student_marks(sid, code, marks)
    print("Marks added successfully!")


def show_student_marks(grade: Grade):
    show_all_student_ids()
    sid = get_int("\nEnter student ID: ")
    grade.get_students_marks(sid)


def show_course_marks(grade: Grade):
    code = get_non_empty_string("\nEnter course code: ").upper()

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

    if sid not in students:
        print("Student not found!")
        return

    details = students[sid].get_student_details()

    print("\n--- Student Details ---")
    for k, v in details.items():
        print(f"{k.capitalize()}: {v}")


def main():
    enrollment = Enrollment()
    grade = Grade()

    print("\n--- Welcome to the Student Course Management System!! ---")

    while True:
        print("\n--- System Menu ---")
        print("1. Add a student")
        print("2. Add a course")
        print("3. Enroll a student in a course")
        print("4. Show all enrollments")
        print("5. Assign grade")
        print("6. Show students marks")
        print("7. Show course marks")
        print("8. List students")
        print("9. List courses")
        print("10. Get student details")
        print("11. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_course()
        elif choice == "3":
            enroll_student(enrollment)
        elif choice == "4":
            enrollment.print_records()
        elif choice == "5":
            assign_grade(enrollment, grade)
        elif choice == "6":
            show_student_marks(grade)
        elif choice == "7":
            show_course_marks(grade)
        elif choice == "8":
            list_students()
        elif choice == "9":
            list_courses()
        elif choice == "10":
            get_student_details()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
