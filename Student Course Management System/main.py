from typing import Iterable
from grade import Grade
from student import GraduateStudent, UndergraduateStudent
from course import Course
from enrollment import Enrollment
from data_store import students, courses


def main():
    enrollment = Enrollment()
    grade = Grade()

    def get_int(prompt: str):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Enter a valid number!")

    def get_float(prompt: str):
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Enter valid marks!")

    def choose_level(type: str) -> int:
        while True:
            print(f"\nEnter {type} level of study:")
            print("1. Undergraduate")
            print("2. Graduate")
            level_choice = get_int("Choose an option: ")
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

    def get_student_course(sid):
        student = students[sid]

        all_courses = list(courses.values())
        filtered_courses = [c for c in all_courses if c.level == student.level]

        if not filtered_courses:
            print(f"\nNo courses available for {student.level}.")
            return False

        return filtered_courses

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
        print("10. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            level_choice = choose_level("student")

            if level_choice == 2:
                topic = input("\nEnter thesis topic: ")
                name = input("Enter student name: ")
                student = GraduateStudent(topic, name)
            else:
                name = input("Enter student name: ")
                student = UndergraduateStudent(name)

            students[student.student_id] = student
            print(f"Student added successfully! Assigned ID = {student.student_id}")
            continue

        if choice == "2":
            level_choice = choose_level("course")

            code = input("\nEnter course code: ").upper()
            title = input("Enter course title: ")

            level = "Undergraduate" if level_choice == 1 else "Graduate"
            courses[code] = Course(code, title, level)

            print("Course added successfully!")
            continue

        if choice == "3":
            show_all_student_ids()
            sid = get_int("\nEnter student ID: ")

            if sid not in students:
                print("Student not found!")
                continue

            filtered_courses = get_student_course(sid)
            if not filtered_courses:
                continue

            print("\nAvailable courses:")
            for c in filtered_courses:
                print(f" - {c.code} : {c.title}")

            code = input("Enter course code to enroll: ").upper()

            if code not in courses:
                print("Course not found!")
                continue

            enrollment.enroll(students[sid], courses[code])
            print("Enrollment successful!")
            continue

        if choice == "4":
            enrollment.print_records()

        if choice == "5":
            show_all_student_ids()
            sid = get_int("\nEnter student ID: ")

            if sid not in students:
                print("Student not found!")
                continue

            filtered_courses = get_student_course(sid)
            if not filtered_courses:
                continue

            print("\nAvailable courses:")
            for c in filtered_courses:
                print(f" - {c.code} : {c.title}")

            code = input("Enter course code: ").upper()

            if (
                sid not in enrollment.records
                or courses[code] not in enrollment.records[sid]
            ):
                print("First enroll this student in this course!")
                continue

            marks = get_float("Enter student marks: ")

            grade.add_student_marks(sid, code, marks)
            print("Marks added successfully!")

        if choice == "6":
            show_all_student_ids()
            sid = get_int("\nEnter student ID: ")

            grade.get_students_marks(sid)

        if choice == "7":
            code = input("\nEnter course code: ").upper()

            if code not in courses:
                print("Course not found!")
                continue

            grade.get_course_student_marks(code)

        if choice == "8":
            if not students:
                print("No students found.")
                continue
            print("\n--- All Students ---")
            for s in students.values():
                print(f" {s}")

        if choice == "9":
            if not courses:
                print("No courses found.")
                continue
            print("\n--- All Courses ---")
            for c in courses.values():
                print(f" - {c}")

        if choice == "10":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
