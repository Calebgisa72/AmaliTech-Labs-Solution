import re
from typing import Optional, Dict


class LogParser:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)

    def parse_line(self, line: str) -> Optional[Dict]:
        """Parses a single line of log."""
        return None
