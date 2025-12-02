import pytest
import data_store
from main import (
    choose_level,
    add_student,
    add_course,
    get_student_courses,
)
from student import UndergraduateStudent, GraduateStudent
from course import Course


@pytest.fixture(autouse=True)
def reset_data():
    data_store.students.clear()
    data_store.courses.clear()


def test_choose_level_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")
    assert choose_level("student") == 1


def test_choose_level_invalid_then_valid(monkeypatch):
    inputs = iter(["5", "2"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    assert choose_level("student") == 2


def test_add_undergraduate_student(monkeypatch):
    # choose undergraduate (1)
    inputs = iter(["1", "John"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_student()
    assert len(data_store.students) == 1

    s = list(data_store.students.values())[0]
    assert isinstance(s, UndergraduateStudent)
    assert s.name == "John"


def test_add_course(monkeypatch):
    inputs = iter(["1", "CS101", "Intro to CS"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    add_course()

    assert "CS101" in data_store.courses
    c = data_store.courses["CS101"]
    assert isinstance(c, Course)
    assert c.title == "Intro to CS"


def test_get_student_courses():
    s = UndergraduateStudent("Alice")
    data_store.students[s.student_id] = s

    c1 = Course("CS101", "Intro", "Undergraduate")
    c2 = Course("GR500", "Grad Course", "Graduate")
    data_store.courses[c1.code] = c1
    data_store.courses[c2.code] = c2

    available = get_student_courses(s.student_id)
    assert available == [c1]
