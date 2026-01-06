import matplotlib.pyplot as plot
from typing import List, Dict, Union
from pathlib import Path
from ..models.student import Student


class VisualizationService:
    @staticmethod
    def generate_grade_distribution_chart(grades: List[float], output_dir: Path):
        """
        Generates a histogram of grade distributions.
        """
        plot.figure(figsize=(10, 6))
        plot.hist(grades, bins=10, edgecolor="black", alpha=0.7)
        plot.title("Grade Distribution")
        plot.xlabel("Grade")
        plot.ylabel("Frequency")
        plot.grid(axis="y", alpha=0.5)

        output_path = output_dir / "grade_distribution.png"
        plot.savefig(output_path)
        plot.close()

    @staticmethod
    def generate_summary_chart(stats: Dict[str, Union[float, str]], output_dir: Path):
        """
        Generates a bar chart for summary statistics (Mean, Median, Mode).
        """
        # Filter out non-numeric values
        numeric_stats = {k: v for k, v in stats.items() if isinstance(v, (int, float))}

        if not numeric_stats:
            return

        plot.figure(figsize=(8, 6))
        plot.bar(
            numeric_stats.keys(),
            numeric_stats.values(),
            color=["blue", "green", "orange"],
        )
        plot.title("Summary Statistics")
        plot.ylabel("Value")

        for i, v in enumerate(numeric_stats.values()):
            plot.text(i, v + 0.5, str(v), ha="center")

        output_path = output_dir / "summary_statistics.png"
        plot.savefig(output_path)
        plot.close()

    @staticmethod
    def generate_top_performers_chart(students: List[Student], output_dir: Path):
        """
        Generates a bar chart for the top 5 performing students based on their average grade.
        """
        student_averages = []
        for student in students:
            grades = [
                c.grade for c in student.courses if isinstance(c.grade, (int, float))
            ]
            if grades:
                avg = sum(grades) / len(grades)
                student_averages.append((student.name, avg))

        student_averages.sort(key=lambda x: x[1], reverse=True)
        top_5 = student_averages[:5]

        if not top_5:
            return

        names = [s[0] for s in top_5]
        averages = [s[1] for s in top_5]

        plot.figure(figsize=(10, 6))
        plot.barh(names, averages, color="purple")
        plot.title("Top 5 Performers")
        plot.xlabel("Average Grade")
        plot.gca().invert_yaxis()

        for i, v in enumerate(averages):
            plot.text(v + 0.1, i, f"{v:.2f}", va="center")

        output_path = output_dir / "top_performers.png"
        plot.savefig(output_path)
        plot.close()
