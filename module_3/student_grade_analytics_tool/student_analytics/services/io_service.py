import csv
from pathlib import Path
from typing import Dict, Any
from contextlib import contextmanager


class IOService:

    @staticmethod
    @contextmanager
    def read_csv(file_path: Path):
        """
        Context manager for reading CSV files.

        Args:
            file_path (Path): Path to the CSV file.

        Yields:
            csv.DictReader: CSV reader object.
        """
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            with open(file_path, mode="r", encoding="utf-8", newline="") as f:
                yield csv.DictReader(f)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise IOError(f"Error reading CSV file: {e}")

    @staticmethod
    def write_json(data: Dict[str, Any], output_path: Path):
        """
        Writes data to a JSON file.

        Args:
            data (Dict): Data to write.
            output_path (Path): Destination path.

        Raises:
            IOError: If there is an issue writing to the file.
        """
        try:
            import json

            if output_path.parent == Path("."):
                output_path = Path("output") / output_path.name

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, mode="w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            raise IOError(f"Error writing JSON file: {e}")
