from models.enrollment import Enrollment
from models.student import UndergraduateStudent
from models.course import Course


def test_enrollment_add_course():
    e = Enrollment()
    s = UndergraduateStudent("Caleb")
    c = Course("CS101", "Intro", "Undergraduate")

    e.enroll(s, c)
    assert e.records[s.student_id][0] == c


def test_get_student_courses_empty():
    e = Enrollment()
    assert e.get_student_courses(99) == []


def test_get_student_courses():
    e = Enrollment()
    s = UndergraduateStudent("Bob")
    c1 = Course("CS101", "Intro", "Undergraduate")
    c2 = Course("MA101", "Math", "Undergraduate")

    e.enroll(s, c1)
    e.enroll(s, c2)

    assert e.get_student_courses(s.student_id) == [c1, c2]
