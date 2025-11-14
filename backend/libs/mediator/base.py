from abc import ABC, abstractmethod
from collections.abc import Iterable


class BaseCommand:
    pass


class BaseEvent:
    pass


class Result[R, E: BaseEvent]:
    result: R
    events: Iterable[E]


EventStore = Iterable[BaseEvent]


class BaseUseCase[C: BaseCommand, R](ABC):
    @abstractmethod
    async def execute(self, command: C) -> Result[R, EventStore]:
        pass


class BaseHandler[E: BaseEvent](ABC):
    @abstractmethod
    async def execute(self, event: E) -> EventStore:
        pass
