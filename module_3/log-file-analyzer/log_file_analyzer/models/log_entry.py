"""
Model for structured log entries.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class LogEntry:
    """Represents a single parsed log line."""

    ip_address: str
    timestamp: str
    request_method: str
    request_url: str
    status_code: int
    user_agent: str
    # Add other fields as necessary
