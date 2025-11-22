from dataclasses import dataclass
from enum import Enum


class CheckStatus(str, Enum):
    ok = "ok"
    error = "error"


@dataclass
class CheckStatusItem:
    service: str
    status: CheckStatus
