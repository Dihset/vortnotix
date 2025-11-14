import pytest

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase
from libs.mediator.registry import (
    BaseCommandRegistry,
    BaseEventRegistry,
    RegistryCommandAlradyRegisteredException,
    RegistryCommandNotFoundException,
    RegistryEventNotFoundException,
)


class Command1(BaseCommand):
    pass


class UseCase1(BaseUseCase):
    async def execute(self, command: BaseCommand):
        pass


class Command2(BaseCommand):
    pass


class UseCase2:
    async def execute(self, command: BaseCommand):
        pass


class TestBaseCommandRegistry:
    def test_success(self):
        registry = BaseCommandRegistry()
        registry.register(Command1, UseCase1)
        registry.register(Command2, UseCase2)
        assert registry.resolve(Command1) == UseCase1
        assert registry.resolve(Command2) == UseCase2

    def test_alrady_registered_exception(self):
        registry = BaseCommandRegistry()
        registry.register(Command1, UseCase1)
        with pytest.raises(RegistryCommandAlradyRegisteredException):
            registry.register(Command1, UseCase2)

    def test_not_found_exception(self):
        registry = BaseCommandRegistry()
        registry.register(Command1, UseCase1)
        with pytest.raises(RegistryCommandNotFoundException):
            registry.resolve(Command2)

    def test_merge(self):
        base_registry = BaseCommandRegistry()
        one_registry = BaseCommandRegistry()
        one_registry.register(Command1, UseCase1)

        two_registry = BaseCommandRegistry()
        two_registry.register(Command2, UseCase2)

        base_registry.merge(one_registry).merge(two_registry)

        assert base_registry.resolve(Command1) == UseCase1
        assert base_registry.resolve(Command2) == UseCase2


class Event1(BaseEvent):
    pass


class Handler1(BaseHandler):
    async def execute(self, event: BaseEvent):
        pass


class Event2(BaseEvent):
    pass


class Handler2(BaseHandler):
    async def execute(self, event: BaseEvent):
        pass


class TestBaseEventRegistry:
    def test_success_one_event(self):
        registry = BaseEventRegistry()
        registry.register(Event1, Handler1)
        registry.register(Event1, Handler2)
        assert Handler1 in registry.resolve(Event1)
        assert Handler2 in registry.resolve(Event1)

    def test_success_many_event(self):
        registry = BaseEventRegistry()
        registry.register(Event1, Handler1)
        registry.register(Event2, Handler2)

        assert Handler1 in registry.resolve(Event1)
        assert Handler2 not in registry.resolve(Event1)

        assert Handler2 in registry.resolve(Event2)
        assert Handler1 not in registry.resolve(Event2)

    def test_not_found_exception(self):
        registry = BaseEventRegistry()
        with pytest.raises(RegistryEventNotFoundException):
            registry.resolve(Event1)

    def test_merge(self):
        base_registry = BaseEventRegistry()

        one_registry = BaseEventRegistry()
        one_registry.register(Event1, Handler1)

        two_registry = BaseEventRegistry()
        two_registry.register(Event2, Handler2)

        base_registry.merge(one_registry).merge(two_registry)

        assert Handler1 in base_registry.resolve(Event1)
        assert Handler2 in base_registry.resolve(Event2)
