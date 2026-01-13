import sys
from resilient_importer.cli import main


def test_cli_success(monkeypatch, valid_csv, tmp_data_dir):
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", str(valid_csv), "--db", str(tmp_data_dir / "users.json")],
    )

    exit_code = main()
    assert exit_code == 0


def test_cli_file_not_found(monkeypatch, tmp_data_dir):
    monkeypatch.setattr(
        sys,
        "argv",
        ["prog", "missing.csv", "--db", str(tmp_data_dir / "users.json")],
    )

    exit_code = main()
    assert exit_code == 1
