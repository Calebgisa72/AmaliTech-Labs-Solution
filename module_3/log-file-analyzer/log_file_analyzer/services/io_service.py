from typing import Generator


class IOService:
    def read_log_file(self, file_path: str) -> Generator[str, None, None]:
        """Reads a log file line by line."""
        yield ""
