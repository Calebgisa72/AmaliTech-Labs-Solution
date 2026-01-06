import pytest
from pathlib import Path
from student_analytics.services.io_service import IOService


def test_read_csv(temp_csv_file):
    with IOService.read_csv(temp_csv_file) as reader:
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["student_id"] == "S101"
        assert rows[1]["student_id"] == "S102"


def test_read_csv_not_found():
    with pytest.raises(FileNotFoundError):
        with IOService.read_csv(Path("non_existent_file.csv")):
            pass


def test_write_json(tmp_path):
    data = {"key": "value", "list": [1, 2, 3]}
    output_path = tmp_path / "output.json"

    IOService.write_json(data, output_path)

    assert output_path.exists()

    import json

    with open(output_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    assert content == data
