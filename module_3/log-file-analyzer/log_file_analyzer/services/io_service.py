from typing import Generator


class IOService:
    @staticmethod
    def read_log_file(file_path: str) -> Generator[str, None, None]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    yield line
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file not found: {file_path}")
        except Exception as e:
            raise IOError(f"Error reading file: {e}")
