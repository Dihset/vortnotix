from collections import defaultdict
from typing import Self

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase


class BaseCommandRegistryException(Exception):
    pass


class RegistryCommandAlradyRegisteredException(BaseCommandRegistryException):
    pass


class RegistryCommandNotFoundException(BaseCommandRegistryException):
    pass


BaseCommandType = type[BaseCommand]
BaseUseCaseType = type[BaseUseCase]


class BaseCommandRegistry:
    def __init__(self):
        self._registry: defaultdict[BaseCommandType, BaseUseCaseType] = defaultdict()

    def register(self, command: BaseCommandType, handler: BaseUseCaseType):
        if command in self._registry:
            raise RegistryCommandAlradyRegisteredException()
        self._registry[command] = handler

    def resolve(self, command: BaseCommandType) -> BaseUseCaseType:
        if command not in self._registry:
            raise RegistryCommandNotFoundException()
        return self._registry[command]

    def merge(self, registry: "BaseCommandRegistry") -> Self:
        for command, use_case in registry._registry.items():
            self.register(command, use_case)
        return self


class BaseEventRegistryException(Exception):
    pass


class RegistryEventNotFoundException(BaseEventRegistryException):
    pass


BaseEventType = type[BaseEvent]
BaseHandlerType = type[BaseHandler]


class BaseEventRegistry:
    def __init__(self):
        self._registry: defaultdict[BaseEventType, list[BaseHandlerType]] = defaultdict()

    def register(self, event: BaseEventType, handler: BaseHandlerType):
        if event not in self._registry:
            self._registry[event] = [handler]
        else:
            self._registry[event].append(handler)

    def resolve(self, event: BaseEventType) -> list[BaseHandlerType]:
        if event not in self._registry:
            raise RegistryEventNotFoundException()
        return self._registry[event]

    def merge(self, registry: "BaseEventRegistry[BaseEventType, BaseHandlerType]") -> Self:
        for event, handler_list in registry._registry.items():
            for handler in handler_list:
                self.register(event, handler)
        return self
