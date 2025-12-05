from models.course import Course


def test_course_creation():
    c = Course("CS101", "Intro to CS", "Undergraduate")
    assert c.code == "CS101"
    assert c.title == "Intro to CS"
    assert c.level == "Undergraduate"


def test_course_str():
    c = Course("CS101", "Intro to CS", "Undergraduate")
    assert str(c) == "CS101: Undergraduate : Intro to CS"
