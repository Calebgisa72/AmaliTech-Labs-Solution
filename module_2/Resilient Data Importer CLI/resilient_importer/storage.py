from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Iterable, Generator, TextIO
from contextlib import contextmanager

from .models.user_model import User
from .exceptions import StorageError

logger = logging.getLogger(__name__)

DATA_DIR = Path.cwd() / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "users.json"


@contextmanager
def read_json(path: Path) -> Generator[list[dict], None, None]:
    try:
        if not path.exists():
            yield []
            return

        with path.open("r", encoding="utf-8") as fh:
            yield json.load(fh)

    except json.JSONDecodeError as e:
        logger.error("JSON decode error for %s", path)
        raise StorageError(f"Bad JSON file: {path}") from e
    except OSError as e:
        logger.error("OS error when opening %s", path)
        raise StorageError(f"Unable to open {path}: {e}") from e


@contextmanager
def write_json(path: Path) -> Generator[TextIO, None, None]:
    try:
        with path.open("w", encoding="utf-8") as fh:
            yield fh
    except OSError as e:
        logger.error("OS error when opening %s", path)
        raise StorageError(f"Unable to open {path}: {e}") from e

class UserRepository:
    def __init__(self, path: Path = DB_FILE):
        self.path = path

    def list_all(self) -> list[User]:
        with read_json(self.path) as raw:
            return [User.from_dict(d) for d in raw]

    def find_by_id(self, user_id: str) -> User | None:
        return next((u for u in self.list_all() if u.user_id == user_id), None)

    def find_by_email(self, email: str) -> User | None:
        email = email.lower()
        return next((u for u in self.list_all() if u.email.lower() == email), None)

    def save_all(self, users: Iterable[User]) -> None:
        with write_json(self.path) as fh:
            json.dump(
                [u.to_dict() for u in users],
                fh,
                indent=2,
                ensure_ascii=False,
            )

    def add(self, user: User) -> None:
        users = self.list_all()
        users.append(user)
        self.save_all(users)
