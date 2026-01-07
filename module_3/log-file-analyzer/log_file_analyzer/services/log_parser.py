import re
from typing import Optional
from log_file_analyzer.models.log_entry import LogEntry


class LogParser:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def parse_line(self, line: str) -> Optional[LogEntry]:
        """
        Parses a single line of log into a LogEntry object.

        Args:
            line: Raw log line string.

        Returns:
            LogEntry object if parsing is successful, None otherwise.
        """
        match = self.pattern.match(line)
        if not match:
            return None

        data = match.groupdict()

        size_str = data.get("size", "0")
        size = 0 if size_str == "-" else int(size_str)

        try:
            status = int(data.get("status", 0))
        except ValueError:
            status = 0

        return LogEntry(
            ip_address=data["ip"],
            identity=data["identity"],
            user_id=data["user"],
            timestamp=data["timestamp"],
            request=data["request"],
            status_code=status,
            size=size,
            referer=data["referer"],
            user_agent=data["user_agent"],
        )
