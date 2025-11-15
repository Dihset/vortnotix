from enum import Enum

from pydantic import BaseModel


class HealthCheckStatus(str, Enum):
    ok = "ok"
    error = "error"


class HealthCheckResult(BaseModel):
    status: HealthCheckStatus = HealthCheckStatus.ok
