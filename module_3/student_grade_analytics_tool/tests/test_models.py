from student_analytics.models.student import Student
from student_analytics.models.course import Course


def test_course_creation():
    c = Course(course_name="Math", credits=3, grade=90.0)
    assert c.course_name == "Math"
    assert c.credits == 3
    assert c.grade == 90.0


def test_student_creation():
    c1 = Course("Math", 3, 90.0)
    s = Student(student_id="S1", name="Alice", major="CS", year=2, courses=[c1])

    assert s.student_id == "S1"
    assert s.name == "Alice"
    assert s.major == "CS"
    assert s.year == 2
    assert len(s.courses) == 1
    assert s.courses[0].course_name == "Math"


def test_student_default_courses():
    s = Student(student_id="S2", name="Bob", major="History", year=1)
    assert s.courses == []
