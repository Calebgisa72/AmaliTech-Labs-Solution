import logging
import sys


def configure_logging(level: int | str = "INFO") -> None:
    fmt = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(fmt))
    root = logging.getLogger()
    root.setLevel(getattr(logging, str(level).upper()))
    root.handlers[:] = [handler]
