from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Protocol

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase
from libs.mediator.registry import BaseCommandRegistry, BaseEventRegistry


class ContainerProtocol[T](Protocol):
    def resolve(self, type_: type[T]) -> T:
        pass


@dataclass
class Mediator:
    command_registry: BaseCommandRegistry
    event_registry: BaseEventRegistry
    container: ContainerProtocol
    # middlewares: list[BaseMediatorMiddleware] = field(default_factory=list)

    def _resolve_use_case(self, command: BaseCommand) -> BaseUseCase:
        class_ = self.command_registry.resolve(type(command))
        return self.container.resolve(class_)

    async def handle(self, command: BaseCommand):
        handler = self._resolve_use_case(command)
        result = await handler.execute(command)
        events_queue = deque()
        events_queue.extend(result.events)
        for event in events_queue:
            await self._handle_event(event, events_queue)

    def _handler_resolve(self, event: BaseEvent) -> Iterable[BaseHandler]:
        classes = self.event_registry.resolve(type(event))
        for class_ in classes:
            yield self.container.resolve(class_)

    async def _handle_event(self, event, events_queue):
        for handler in self._handler_resolve(event):
            events = await handler.execute(event)
            if events:
                events_queue.extend(events)
