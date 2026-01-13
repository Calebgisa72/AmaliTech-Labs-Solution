import pytest

from resilient_importer.models.user_model import User


@pytest.fixture
def valid_user():
    return User(user_id="1", name="Alice", email="alice@example.com")


@pytest.fixture
def another_user():
    return User(user_id="2", name="Bob", email="bob@example.com")


@pytest.fixture
def duplicate_user():
    return User(user_id="1", name="Alice Dup", email="alice@example.com")


@pytest.fixture
def tmp_data_dir(tmp_path):
    """
    Temporary directory for test data.
    Automatically cleaned up by pytest.
    """
    return tmp_path


@pytest.fixture
def valid_csv(tmp_data_dir):
    csv_path = tmp_data_dir / "users.csv"
    csv_path.write_text(
        "user_id,name,email\n" "1,Alice,alice@example.com\n" "2,Bob,bob@example.com\n",
        encoding="utf-8",
    )
    return csv_path


@pytest.fixture
def malformed_csv(tmp_data_dir):
    csv_path = tmp_data_dir / "bad.csv"
    csv_path.write_text(
        "user_id,name,email\n" "1,,alice@example.com\n",
        encoding="utf-8",
    )
    return csv_path


@pytest.fixture
def missing_header_csv(tmp_data_dir):
    csv_path = tmp_data_dir / "missing_headers.csv"
    csv_path.write_text(
        "id,fullname,mail\n" "1,Alice,alice@example.com\n",
        encoding="utf-8",
    )
    return csv_path
