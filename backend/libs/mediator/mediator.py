from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Protocol

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase, Result
from libs.mediator.middleware import BaseMediatorMiddleware
from libs.mediator.registry import BaseCommandRegistry, BaseEventRegistry


class ContainerProtocol[T](Protocol):
    def resolve(self, type_: type[T]) -> T:
        pass


@dataclass
class Mediator:
    command_registry: BaseCommandRegistry
    event_registry: BaseEventRegistry
    container: ContainerProtocol
    middlewares: list[BaseMediatorMiddleware] = field(default_factory=list)

    def _resolve_use_case(self, command: BaseCommand) -> BaseUseCase:
        class_ = self.command_registry.resolve(type(command))
        return self.container.resolve(class_)

    async def _execute_use_case(self, command: BaseCommand, use_case: BaseUseCase) -> Result:
        for middleware in self.middlewares:
            await middleware.pre_run_use_case(command, use_case)

        result = await use_case.execute(command)

        for middleware in self.middlewares:
            await middleware.post_run_use_case(command, use_case, result)

        return result

    async def handle(self, command: BaseCommand):
        use_case = self._resolve_use_case(command)
        result = await self._execute_use_case(command, use_case)
        events_queue = deque()
        events_queue.extend(result.events)
        for event in events_queue:
            await self._handle_event(event, events_queue)

    def _handler_resolve(self, event: BaseEvent) -> Iterable[BaseHandler]:
        classes = self.event_registry.resolve(type(event))
        for class_ in classes:
            yield self.container.resolve(class_)

    async def _execute_handler(self, event: BaseHandler, handler: BaseHandler) -> Iterable[BaseEvent]:
        for middleware in self.middlewares:
            await middleware.pre_run_handler(event, handler)

        events = await handler.execute(event)

        for middleware in self.middlewares:
            await middleware.post_run_handler(event, handler, events)

        return events

    async def _handle_event(self, event, events_queue):
        for handler in self._handler_resolve(event):
            events = await self._execute_handler(event, handler)
            if events:
                events_queue.extend(events)
