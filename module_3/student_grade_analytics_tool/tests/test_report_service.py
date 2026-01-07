from student_analytics.services.report_service import ReportService


def test_generate_report(sample_students):
    report = ReportService.generate_report(sample_students)

    assert "overall_statistics" in report
    assert "grade_distribution" in report
    assert "major_enrollment" in report
    assert "top_performers" in report

    assert report["major_enrollment"]["CS"] == 2
    assert report["major_enrollment"]["Math"] == 1

    # Check top performers structure
    assert len(report["top_performers"]) <= 3
    assert report["top_performers"][0]["name"] == "Charlie"  # 93.5 avg


def test_generate_report_empty():
    report = ReportService.generate_report([])
    assert "error" in report
    assert report["error"] == "No student data available"
