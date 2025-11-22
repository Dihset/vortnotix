from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol, TypeVar

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase
from libs.mediator.middleware import BaseMediatorMiddleware, compose_handler, compose_use_case
from libs.mediator.registry import BaseCommandRegistry, BaseEventRegistry

T = TypeVar("T")


class ContainerProtocol(Protocol):
    def resolve(self, type_: type[T]) -> T:
        pass


@dataclass
class Mediator:
    command_registry: BaseCommandRegistry
    event_registry: BaseEventRegistry
    container: ContainerProtocol
    middlewares: list[BaseMediatorMiddleware] = field(default_factory=list)

    def __post_init__(self):
        self.wrapped_use_case_executer = compose_use_case(self.middlewares)
        self.wrapped_handler_executer = compose_handler(self.middlewares)

    def _resolve_use_case(self, command: BaseCommand) -> BaseUseCase:
        class_ = self.command_registry.resolve(type(command))
        return self.container.resolve(class_)

    async def handle(self, command: BaseCommand):
        use_case = self._resolve_use_case(command)
        result = await self.wrapped_use_case_executer(command, use_case)
        events_queue = deque()
        events_queue.extend(result.events)
        for event in events_queue:
            await self._handle_event(event, events_queue)

        return result.result

    def _handler_resolve(self, event: BaseEvent) -> Iterable[BaseHandler]:
        classes = self.event_registry.resolve(type(event))
        for class_ in classes:
            yield self.container.resolve(class_)

    async def _handle_event(self, event, events_queue):
        for handler in self._handler_resolve(event):
            events = await self.wrapped_handler_executer(event, handler)
            if events:
                events_queue.extend(events)
