import pytest
from unittest.mock import patch
from pathlib import Path
from student_analytics.services.visualization_service import VisualizationService


@pytest.fixture
def mock_plot():
    with patch("student_analytics.services.visualization_service.plot") as mock:
        yield mock


def test_generate_grade_distribution_chart(mock_plot):
    output_dir = Path("output")
    VisualizationService.generate_grade_distribution_chart([90, 80], output_dir)

    mock_plot.hist.assert_called_once()
    mock_plot.savefig.assert_called_once()
    mock_plot.close.assert_called_once()


def test_generate_summary_chart(mock_plot):
    output_dir = Path("output")
    stats = {"mean": 85, "median": 80, "mode": "Multimodal"}

    VisualizationService.generate_summary_chart(stats, output_dir)

    mock_plot.bar.assert_called_once()
    mock_plot.savefig.assert_called_once()
    # mode is string, should be filtered out
    args, _ = mock_plot.bar.call_args
    assert len(list(args[0])) == 2  # mean and median only


def test_generate_summary_chart_empty(mock_plot):
    output_dir = Path("output")
    stats = {}
    VisualizationService.generate_summary_chart(stats, output_dir)
    mock_plot.bar.assert_not_called()


def test_generate_top_performers_chart(mock_plot, sample_students):
    output_dir = Path("output")
    VisualizationService.generate_top_performers_chart(sample_students, output_dir)

    mock_plot.barh.assert_called_once()
    mock_plot.savefig.assert_called_once()


def test_generate_top_performers_chart_no_students(mock_plot):
    output_dir = Path("output")
    VisualizationService.generate_top_performers_chart([], output_dir)
    mock_plot.barh.assert_not_called()
