from student_analytics.main import parse_student_row
from student_analytics.models.student import Student


def test_parse_student_row():
    row = {
        "student_id": "S999",
        "name": "Integration Test Student",
        "major": "Biology",
        "year": "3",
        "course_name": "Genetics",
        "credits": "4",
        "grade": "88.5",
    }

    student = parse_student_row(row)

    assert isinstance(student, Student)
    assert student.student_id == "S999"
    assert student.name == "Integration Test Student"
    assert student.major == "Biology"
    assert student.year == 3
    assert len(student.courses) == 1
    assert student.courses[0].course_name == "Genetics"
    assert student.courses[0].credits == 4
    assert student.courses[0].grade == 88.5


def test_parse_student_row_invalid_grade():
    row = {
        "student_id": "S998",
        "name": "Bad Grade Student",
        "major": "Chem",
        "year": "2",
        "course_name": "Chemistry 101",
        "credits": "3",
        "grade": "NotAGrade",
    }

    student = parse_student_row(row)

    assert student.courses[0].grade == 0.0
