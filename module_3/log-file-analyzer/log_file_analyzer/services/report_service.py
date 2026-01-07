from typing import Dict, List, Tuple


class ReportService:

    def generate_text_report(
        self,
        status_counts: Dict[int, int],
        total_size: int,
        top_ips: List[Tuple[str, int]],
    ) -> str:
        report_lines = []
        report_lines.append("=" * 40)
        report_lines.append("LOG ANALYSIS REPORT")
        report_lines.append("=" * 40)

        report_lines.append("\n[Status Code Distribution]")
        for code, count in sorted(status_counts.items()):
            report_lines.append(f"  {code}: {count}")

        report_lines.append("\n[Traffic Stats]")
        report_lines.append(f"  Total Data Transfer: {total_size / (1024*1024):.2f} MB")

        report_lines.append("\n[Top Active IPs]")
        for ip, count in top_ips:
            report_lines.append(f"  {ip}: {count} requests")

        report_lines.append("\n" + "=" * 40)
        return "\n".join(report_lines)
