import pytest

from resilient_importer.parser import parse_csv
from resilient_importer.exceptions import (
    CSVFileNotFoundError,
    FileFormatError,
)


def test_parse_csv_success(valid_csv):
    users = list(parse_csv(str(valid_csv)))

    assert len(users) == 2
    assert users[0].user_id == "1"
    assert users[1].email == "bob@example.com"


def test_parse_csv_file_not_found():
    with pytest.raises(CSVFileNotFoundError):
        list(parse_csv("nonexistent.csv"))


def test_parse_csv_missing_headers(missing_header_csv):
    with pytest.raises(FileFormatError):
        list(parse_csv(str(missing_header_csv)))


def test_parse_csv_malformed_row(malformed_csv):
    with pytest.raises(FileFormatError):
        list(parse_csv(str(malformed_csv)))
