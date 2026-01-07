import pytest
from student_analytics.services.analysis_service import AnalysisService
from student_analytics.models.student import Student
from student_analytics.models.course import Course


@pytest.mark.parametrize(
    "grades, expected",
    [
        ([90, 90, 80], {90: 2, 80: 1}),
        ([], {}),
        ([100], {100: 1}),
    ],
)
def test_calculate_distribution(grades, expected):
    result = AnalysisService.calculate_distribution(grades)
    assert dict(result) == expected


def test_group_by_major(sample_students):
    result = AnalysisService.group_by_major(sample_students)

    assert "CS" in result
    assert "Math" in result
    assert len(result["CS"]) == 2
    assert len(result["Math"]) == 1
    assert result["CS"][0].name == "Alice"
    assert result["CS"][1].name == "Charlie"


def test_overall_statistics(sample_students):
    stats = AnalysisService.overall_statistics(sample_students)

    # Alice: 90, 85 -> 87.5
    # Bob: 75, 80 -> 77.5
    # Charlie: 90, 92 -> 91.0
    # All grades: 90, 85, 75, 80, 90, 92
    # Mean: 512 / 6 = 85.33
    # Sorted: 75, 80, 85, 90, 90, 92
    # Median: (85 + 90) / 2 = 87.5
    # Mode: 90.0

    assert stats["mean"] == 85.33
    assert stats["median"] == 87.5
    assert stats["mode"] == 90.0


def test_overall_statistics_empty():
    stats = AnalysisService.overall_statistics([])
    assert stats["mean"] == 0.0
    assert stats["median"] == 0.0
    assert stats["mode"] == 0.0


def test_overall_statistics_single_mode():
    s = Student("S4", "Dave", "Art", 1, [Course("Art", 3, 80), Course("Design", 3, 80)])
    stats = AnalysisService.overall_statistics([s])
    assert stats["mode"] == 80
