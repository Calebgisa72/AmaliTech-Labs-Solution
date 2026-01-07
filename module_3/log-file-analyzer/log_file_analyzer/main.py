import sys
from pathlib import Path
from log_file_analyzer.config import Config
from log_file_analyzer.services.io_service import IOService
from log_file_analyzer.services.log_parser import LogParser
from log_file_analyzer.services.analysis_service import AnalysisService
from log_file_analyzer.services.report_service import ReportService


def main():
    print("Starting Log File Analyzer...")

    import argparse

    parser = argparse.ArgumentParser(description="Analyze web server access logs.")
    parser.add_argument(
        "file_path",
        nargs="?",
        default="sample.log",
        help="Path to the log file to analyze (default: sample.log)",
    )
    args = parser.parse_args()

    log_file_path = args.file_path

    if not Path(log_file_path).exists():
        print(f"Error: Log file '{log_file_path}' not found.")
        print("Please provide a valid log file path or create a 'sample.log'.")
        sys.exit(1)

    io_service = IOService()
    log_parser = LogParser(Config.LOG_PATTERN)
    report_service = ReportService()

    try:
        raw_lines = io_service.read_log_file(log_file_path)

        parsed_logs_gen = (log_parser.parse_line(line) for line in raw_lines)
        valid_logs_gen = (log for log in parsed_logs_gen if log is not None)

        print("Reading and parsing logs...")
        logs = list(valid_logs_gen)
        print(f"Parsed {len(logs)} valid log entries.")

        if not logs:
            print("No valid logs found.")
            return

        print("Performing analysis...")
        status_counts = AnalysisService.count_status_codes(logs)
        total_size = AnalysisService.calculate_total_size(logs)
        top_ips = AnalysisService.get_top_ips(logs)

        report = report_service.generate_text_report(status_counts, total_size, top_ips)
        print(report)

    except Exception as e:
        print(f"An error occurred during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
