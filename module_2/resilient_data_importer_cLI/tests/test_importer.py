from resilient_importer.importer import Importer
from resilient_importer.storage import UserRepository


def test_importer_success(valid_csv, tmp_data_dir):
    repo = UserRepository(tmp_data_dir / "users.json")
    importer = Importer(repo)

    summary = importer.import_from_csv(str(valid_csv))

    assert summary["imported"] == 2
    assert summary["duplicates"] == 0
    assert summary["errors"] == []


def test_importer_duplicates(valid_csv, tmp_data_dir):
    repo = UserRepository(tmp_data_dir / "users.json")
    importer = Importer(repo)

    importer.import_from_csv(str(valid_csv))
    summary = importer.import_from_csv(str(valid_csv))

    assert summary["imported"] == 0
    assert summary["duplicates"] == 2


def test_importer_csv_not_found(tmp_data_dir):
    repo = UserRepository(tmp_data_dir / "users.json")
    importer = Importer(repo)

    summary = importer.import_from_csv("missing.csv")

    assert summary["imported"] == 0
    assert summary["errors"]
