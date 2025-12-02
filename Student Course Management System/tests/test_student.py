import pytest
from student import GraduateStudent, UndergraduateStudent, Student


@pytest.fixture(autouse=True)
def reset_student_ids():
    Student._next_id = 1


def test_undergraduate_student_creation():
    s = UndergraduateStudent("Caleb")
    assert s.name == "Caleb"
    assert s.level == "Undergraduate"
    assert s.get_student_details() == {
        "student_id": 1,
        "name": "Caleb",
        "level": "Undergraduate",
    }


def test_graduate_student_creation():
    s = GraduateStudent("AI Research", "Bob")
    assert s.name == "Bob"
    assert s.thesis_topic == "AI Research"
    assert s.level == "Graduate"
    assert s.get_student_details() == {
        "student_id": 1,
        "name": "Bob",
        "level": "Graduate",
        "thesis_topic": "AI Research",
    }


def test_student_str_representation():
    s = UndergraduateStudent("Charlie")
    assert str(s) == "1 - Charlie (Undergraduate)"
