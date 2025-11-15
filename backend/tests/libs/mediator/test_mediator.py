from dataclasses import dataclass

import punq
import pytest

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase, EventStore, Result
from libs.mediator.mediator import ContainerProtocol, Mediator
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

    async def execute(self, command: Command) -> Result[None, EventStore]:
        self.checker.use_case_runned = True
        return Result(result=None, events=[Event()])


@dataclass
class Handler(BaseHandler[Event]):
    checker: Checker

    async def execute(self, event: Event) -> EventStore:
        self.checker.handler_runned = True


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
    )


class TestMediator:
    async def test_success(self, mediator: Mediator):
        result = await mediator.handle(Command())

        assert result is None

        checker: Checker = mediator.container.resolve(Checker)
        assert checker.use_case_runned
        assert checker.handler_runned
