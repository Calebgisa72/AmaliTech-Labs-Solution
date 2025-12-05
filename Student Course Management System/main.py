from models.grade import Grade
from models.enrollment import Enrollment
import controllers as ctrl


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
            ctrl.add_student()
        elif choice == "2":
            ctrl.add_course()
        elif choice == "3":
            ctrl.enroll_student(enrollment)
        elif choice == "4":
            enrollment.print_records()
        elif choice == "5":
            ctrl.assign_grade(enrollment, grade)
        elif choice == "6":
            ctrl.show_student_marks(grade)
        elif choice == "7":
            ctrl.show_course_marks(grade)
        elif choice == "8":
            ctrl.list_students()
        elif choice == "9":
            ctrl.list_courses()
        elif choice == "10":
            ctrl.get_student_details()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
