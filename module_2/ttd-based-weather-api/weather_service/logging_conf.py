import logging
import sys


def configure_logging(level: str | int = "INFO") -> None:
    """
    Configure application-wide logging.

    - Sets log level (default = INFO)
    - Writes logs to stdout (not stderr)
    - Applies consistent formatting
    - Avoids duplicate handlers
    """

    log_format = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))

    root = logging.getLogger()
    root.setLevel(str(level).upper())
    root.handlers = [handler]
