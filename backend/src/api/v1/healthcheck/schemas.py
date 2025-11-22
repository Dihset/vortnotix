from typing import Self

from pydantic import BaseModel, RootModel

from src.modules.base.domain.entities import CheckStatus, CheckStatusItem


class HealthCheckResult(BaseModel):
    status: CheckStatus = CheckStatus.ok


class ReadinessCheckItem(BaseModel):
    service: str
    status: CheckStatus

    @classmethod
    def from_entity(cls, entity: CheckStatusItem) -> Self:
        return cls(
            service=entity.service,
            status=entity.status,
        )


class ReadinessCheckResult(RootModel[list[ReadinessCheckItem]]):
    @classmethod
    def from_entity(cls, entities: list[CheckStatusItem]) -> Self:
        return cls([ReadinessCheckItem.from_entity(item) for item in entities])
