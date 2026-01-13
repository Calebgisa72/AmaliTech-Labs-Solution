import csv
from typing import Iterator
from pathlib import Path

from .models.user_model import User
from .exceptions import FileFormatError, CSVFileNotFoundError
import logging

logger = logging.getLogger(__name__)


def parse_csv(path: str) -> Iterator[User]:
    """
    Parse CSV and yield User objects.

    Expected CSV headers: user_id, name, email.
    Raises CSVFileNotFoundError if file missing.
    Raises FileFormatError for malformed rows.
    """
    p = Path(path)
    if not p.exists():
        raise CSVFileNotFoundError(f"CSV file not found: {path}")

    with p.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        expected = {"user_id", "name", "email"}
        if not expected.issubset(set(reader.fieldnames or [])):
            raise FileFormatError("CSV missing required headers (user_id,name,email)")

        for i, row in enumerate(reader, start=2):
            try:
                uid = row.get("user_id", "").strip()
                name = row.get("name", "").strip()
                email = row.get("email", "").strip()
                if not uid or not name or not email:
                    raise ValueError("Empty required field")
                yield User(user_id=uid, name=name, email=email)
            except Exception as e:
                logger.error("Malformed CSV row at line %s: %s", i, e)
                raise FileFormatError(f"Malformed CSV row at line {i}: {e}") from e
