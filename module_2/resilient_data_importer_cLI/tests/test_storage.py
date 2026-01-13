import pytest

from resilient_importer.storage import UserRepository
from resilient_importer.exceptions import StorageError


def test_repository_add_and_list(tmp_data_dir, valid_user):
    db_path = tmp_data_dir / "users.json"
    repo = UserRepository(db_path)

    repo.add(valid_user)
    users = repo.list_all()

    assert len(users) == 1
    assert users[0].email == valid_user.email


def test_find_by_id_and_email(tmp_data_dir, valid_user):
    repo = UserRepository(tmp_data_dir / "users.json")
    repo.add(valid_user)

    assert repo.find_by_id("1") is not None
    assert repo.find_by_email("alice@example.com") is not None


def test_read_invalid_json(tmp_data_dir):
    bad_json = tmp_data_dir / "users.json"
    bad_json.write_text("{ invalid json", encoding="utf-8")

    repo = UserRepository(bad_json)

    with pytest.raises(StorageError):
        repo.list_all()
