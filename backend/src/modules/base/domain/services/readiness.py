from abc import ABC, abstractmethod

from src.modules.base.domain.entities import CheckStatusItem


class IReadinessService(ABC):
    @abstractmethod
    async def is_ready(self) -> list[CheckStatusItem]:
        pass
