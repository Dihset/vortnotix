from ast import TypeVar
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import cast

import punq
import pytest

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase, EventStore, Result
from libs.mediator.mediator import ContainerProtocol, Mediator
from libs.mediator.middleware import BaseMediatorMiddleware
from libs.mediator.registry import BaseCommandRegistry, BaseEventRegistry


class Checker:
    use_case_runned: bool = False
    handler_runned: bool = False


class Command(BaseCommand):
    pass


class Event(BaseEvent):
    pass


@dataclass
class UseCase(BaseUseCase[Command, None]):
    checker: Checker

    async def execute(self, command: Command) -> Result[None]:
        self.checker.use_case_runned = True
        return Result(result=None, events=[Event()])


@dataclass
class Handler(BaseHandler[Event]):
    checker: Checker

    async def execute(self, event: Event) -> EventStore | None:
        self.checker.handler_runned = True


R = TypeVar("R")


@dataclass
class CheckerMiddleware(BaseMediatorMiddleware):
    pre_run_use_case_called: bool = False
    post_run_use_case_called: bool = False
    pre_run_handler_called: bool = False
    post_run_handler_called: bool = False

    async def wrap_use_case(
        self,
        command: BaseCommand,
        use_case: BaseUseCase,
        call_next: Callable[[BaseCommand, BaseUseCase], Awaitable[Result[R]]],
    ) -> Result[R]:
        self.pre_run_use_case_called = True
        result = await call_next(command, use_case)
        self.post_run_use_case_called = True
        return result

    async def wrap_handler(
        self,
        event: BaseEvent,
        handler: BaseHandler,
        call_next: Callable[[BaseEvent, BaseHandler], Awaitable[EventStore | None]],
    ) -> EventStore | None:
        self.pre_run_handler_called = True
        result = await call_next(event, handler)
        self.post_run_handler_called = True
        return result


@pytest.fixture
def container() -> ContainerProtocol:
    container = punq.Container()
    container.register(Checker, scope=punq.Scope.singleton)
    container.register(UseCase)
    container.register(Handler)
    return container


@pytest.fixture
def command_registry() -> BaseCommandRegistry:
    registry = BaseCommandRegistry()
    registry.register(Command, UseCase)
    return registry


@pytest.fixture
def event_registry() -> BaseEventRegistry:
    registry = BaseEventRegistry()
    registry.register(Event, Handler)
    return registry


@pytest.fixture
def mediator(
    container: ContainerProtocol,
    command_registry: BaseCommandRegistry,
    event_registry: BaseEventRegistry,
) -> Mediator:
    return Mediator(
        command_registry=command_registry,
        event_registry=event_registry,
        container=container,
        middlewares=[CheckerMiddleware()],
    )


class TestMediator:
    async def test_success(self, mediator: Mediator):
        result = await mediator.handle(Command())

        assert result is None

        checker: Checker = mediator.container.resolve(Checker)
        assert checker.use_case_runned
        assert checker.handler_runned

        checker_middleware = cast(CheckerMiddleware, mediator.middlewares[0])
        assert checker_middleware.pre_run_use_case_called
        assert checker_middleware.post_run_use_case_called
        assert checker_middleware.pre_run_handler_called
        assert checker_middleware.post_run_handler_called
