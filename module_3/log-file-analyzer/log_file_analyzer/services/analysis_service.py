from typing import Iterable, Dict, List, Tuple
from functools import reduce
from itertools import groupby
from collections import Counter
from log_file_analyzer.models.log_entry import LogEntry
from log_file_analyzer.utils.decorators import timer, log_call


class AnalysisService:
    @staticmethod
    @timer
    @log_call
    def count_status_codes(logs: Iterable[LogEntry]) -> Dict[int, int]:
        """
        Counts the occurrence of each status code.
        """

        # Map to status codes
        status_codes = map(lambda log: log.status_code, logs)

        return dict(Counter(status_codes))

    @staticmethod
    @timer
    def calculate_total_size(logs: Iterable[LogEntry]) -> int:
        return reduce(lambda acc, log: acc + log.size, logs, 0)

    @staticmethod
    @timer
    def get_top_ips(logs: Iterable[LogEntry], top_n: int = 5) -> List[Tuple[str, int]]:
        """Returns top N IP addresses by request count."""
        ips = map(lambda log: log.ip_address, logs)
        return Counter(ips).most_common(top_n)

    @staticmethod
    @timer
    def filter_by_min_size(
        logs: Iterable[LogEntry], min_size: int
    ) -> Iterable[LogEntry]:
        """Filters logs with size greater than min_size."""
        return filter(lambda log: log.size >= min_size, logs)

    @staticmethod
    @timer
    def group_by_status_code(logs: Iterable[LogEntry]) -> Dict[int, List[LogEntry]]:
        """Groups logs by status code using itertools.groupby."""
        # groupby requires sorted input
        sorted_logs = sorted(list(logs), key=lambda x: x.status_code)

        grouped = {}
        for key, group in groupby(sorted_logs, key=lambda x: x.status_code):
            grouped[key] = list(group)

        return grouped
