from __future__ import annotations
import logging
from typing import List, TypedDict

from .parser import parse_csv
from .storage import UserRepository
from .exceptions import ImporterError

logger = logging.getLogger(__name__)


class ImportSummary(TypedDict):
    imported: int
    duplicates: int
    errors: List[str]


class Importer:
    def __init__(self, repo: UserRepository | None = None):
        self.repo = repo or UserRepository()

    def import_from_csv(self, csv_path: str) -> ImportSummary:
        summary: ImportSummary = {
            "imported": 0,
            "duplicates": 0,
            "errors": [],
        }

        try:
            for user in parse_csv(csv_path):
                try:
                    if (
                        self.repo.find_by_id(user.user_id) is not None
                        or self.repo.find_by_email(user.email) is not None
                    ):
                        summary["duplicates"] += 1
                        logger.warning("Duplicate user skipped: %s", user)
                        continue

                    self.repo.add(user)
                    summary["imported"] += 1
                    logger.info("Imported user: %s", user)

                except Exception as e:
                    logger.error("Error while adding user %s: %s", user, e)
                    summary["errors"].append(f"{user.user_id}: {e}")

        except ImporterError as e:
            logger.error("Importer aborted due to error: %s", e)
            summary["errors"].append(str(e))

        return summary
