import argparse
import sys
import logging
from pathlib import Path

from .models.student import Student
from .models.course import Course
from .services.io_service import IOService
from .services.report_service import ReportService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def parse_student_row(row: dict) -> Student:
    try:
        grade_val = float(row["grade"])
    except ValueError:
        grade_val = 0.0

    course = Course(
        course_name=row["course_name"], credits=int(row["credits"]), grade=grade_val
    )

    return Student(
        student_id=row["student_id"],
        name=row["name"],
        major=row["major"],
        year=int(row["year"]),
        courses=[course],
    )


def main():
    parser = argparse.ArgumentParser(description="Student Grade Analytics Tool")
    parser.add_argument("input_file", type=Path, help="Path to input CSV file")
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("output/report.json"),
        help="Path to output JSON report",
    )

    args = parser.parse_args()

    if not args.input_file.exists():
        logger.error(f"Input file '{args.input_file}' does not exist.")
        sys.exit(1)

    logger.info(f"Processing {args.input_file}...")

    students_map = {}

    try:
        with IOService.read_csv(args.input_file) as reader:
            for row in reader:
                required_cols = [
                    "student_id",
                    "name",
                    "major",
                    "year",
                    "course_name",
                    "credits",
                    "grade",
                ]
                if not all(col in row for col in required_cols):
                    logger.warning(f"Skipping malformed row: {row}")
                    continue

                student_temp = parse_student_row(row)

                if student_temp.student_id in students_map:
                    students_map[student_temp.student_id].courses.extend(
                        student_temp.courses
                    )
                else:
                    students_map[student_temp.student_id] = student_temp

        students = list(students_map.values())
        logger.info(f"Loaded {len(students)} students.")

        logger.info("Generating report...")
        report = ReportService.generate_report(students)

        IOService.write_json(report, args.output)
        logger.info(f"Report saved to {args.output}")

        logger.info("Generating visualizations...")
        output_dir = args.output.parent
        if output_dir == Path("."):
            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)

        all_grades = [
            course.grade
            for student in students
            for course in student.courses
            if isinstance(course.grade, (int, float))
        ]

        from .services.visualization_service import VisualizationService

        VisualizationService.generate_grade_distribution_chart(all_grades, output_dir)
        VisualizationService.generate_summary_chart(
            report["overall_statistics"], output_dir
        )
        VisualizationService.generate_top_performers_chart(students, output_dir)

        logger.info(f"Visualizations saved to {output_dir}")

    except Exception:
        logger.exception("An unexpected error occurred")
        sys.exit(1)


if __name__ == "__main__":
    main()
