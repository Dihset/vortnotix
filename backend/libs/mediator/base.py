from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass, field


class BaseCommand:
    pass


class BaseEvent:
    pass


EventStore = Sequence[BaseEvent]


@dataclass
class Result[R]:
    result: R
    events: EventStore = field(default_factory=list)


class BaseUseCase[C: BaseCommand, R](ABC):
    @abstractmethod
    async def execute(self, command: C) -> Result[R]:
        pass


class BaseHandler[E: BaseEvent](ABC):
    @abstractmethod
    async def execute(self, event: E) -> EventStore | None:
        pass
