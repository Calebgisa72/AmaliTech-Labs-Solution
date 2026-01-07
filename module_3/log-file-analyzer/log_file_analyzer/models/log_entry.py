from dataclasses import dataclass


@dataclass
class LogEntry:
    ip_address: str
    identity: str
    user_id: str
    timestamp: str
    request: str
    status_code: int
    size: int
    referer: str
    user_agent: str
