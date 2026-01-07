import pytest
from student_analytics.models.student import Student
from student_analytics.models.course import Course
import csv


@pytest.fixture
def sample_students():
    s1 = Student(
        student_id="S001",
        name="Alice",
        major="CS",
        year=2,
        courses=[Course("Math", 3, 90.0), Course("Physics", 4, 85.0)],
    )
    s2 = Student(
        student_id="S002",
        name="Bob",
        major="Math",
        year=3,
        courses=[Course("Math", 3, 75.0), Course("History", 2, 80.0)],
    )
    s3 = Student(
        student_id="S003",
        name="Charlie",
        major="CS",
        year=1,
        courses=[Course("Math", 3, 90.0), Course("Physics", 4, 92.0)],
    )
    return [s1, s2, s3]


@pytest.fixture
def temp_csv_file(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    p = d / "test_students.csv"

    headers = ["student_id", "name", "major", "year", "course_name", "credits", "grade"]
    data = [
        ["S101", "Test User", "Physics", "1", "Intro Physics", "3", "88.5"],
        ["S102", "Another User", "Bio", "2", "Biology 101", "4", "92.0"],
    ]

    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

    return p
