import pytest
import data_store
from models.grade import Grade
from models.student import UndergraduateStudent
from models.course import Course


@pytest.fixture
def setup_data():
    data_store.students.clear()
    data_store.courses.clear()

    s = UndergraduateStudent("Alice")
    c = Course("CS101", "Intro", "Undergraduate")

    data_store.students[s.student_id] = s
    data_store.courses[c.code] = c

    return s, c


def test_add_student_marks(setup_data):
    s, c = setup_data
    g = Grade()

    g.add_student_marks(s.student_id, c.code, 85.5)
    assert g.grades[s.student_id][c.code] == 85.5


def test_get_students_marks_output(setup_data, capsys):
    s, c = setup_data
    g = Grade()
    g.add_student_marks(s.student_id, c.code, 90)

    g.get_students_marks(s.student_id)
    captured = capsys.readouterr().out

    assert "Marks for Alice:" in captured
    assert "Intro: 90" in captured
    assert "Average" in captured


def test_get_course_student_marks_output(setup_data, capsys):
    s, c = setup_data
    g = Grade()
    g.add_student_marks(s.student_id, c.code, 70)

    g.get_course_student_marks(c.code)
    captured = capsys.readouterr().out

    assert "Marks for Intro:" in captured
    assert "Alice: 70" in captured
