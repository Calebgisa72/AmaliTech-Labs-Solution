from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


@dataclass
class User:
    user_id: str
    name: str
    email: str

    def to_dict(self) -> Dict[str, str]:
        return {"user_id": self.user_id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, d: Dict[str, str]) -> "User":
        return cls(user_id=d["user_id"], name=d["name"], email=d["email"])
