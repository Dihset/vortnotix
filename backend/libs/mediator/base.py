from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass


class BaseCommand:
    pass


class BaseEvent:
    pass


EventStore = Sequence[BaseEvent]


@dataclass
class Result[R]:
    result: R
    events: EventStore


class BaseUseCase[C: BaseCommand, R](ABC):
    @abstractmethod
    async def execute(self, command: C) -> Result[R]:
        pass


class BaseHandler[E: BaseEvent](ABC):
    @abstractmethod
    async def execute(self, event: E) -> EventStore | None:
        pass
