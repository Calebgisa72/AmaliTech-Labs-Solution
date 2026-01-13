import argparse
import logging
import sys
from pathlib import Path

from .importer import Importer
from .storage import UserRepository
from .logging_conf import configure_logging

configure_logging()

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Command-line entry point for the resilient importer.
    Returns an exit code:
      0 -> success
      1 -> failure
    """

    parser = argparse.ArgumentParser(
        description="Import users from a CSV file into JSON storage"
    )

    parser.add_argument("csvfile", help="Path to the CSV file to import")
    parser.add_argument(
        "--db", help="Optional path to JSON database file", default=None
    )

    args = parser.parse_args()

    try:
        if args.db is None:
            repo = UserRepository()
        else:
            repo = UserRepository(Path(args.db))
    except Exception as e:
        logger.error("Failed to initialize storage")
        print(f"Storage error: {e}")
        return 1

    importer = Importer(repo)

    logger.info("Starting import from %s", args.csvfile)

    try:
        summary = importer.import_from_csv(args.csvfile)
    except Exception as e:
        logger.error("Import failed")
        print(f"Import failed: {e}")
        return 1

    print("\nImport Summary")
    print("-" * 20)
    print(f"Imported:   {summary['imported']}")
    print(f"Duplicates: {summary['duplicates']}")

    if summary["errors"]:
        print("Errors:")
        for error in summary["errors"]:
            print(f" - {error}")

    logger.info("Import finished successfully")

    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
