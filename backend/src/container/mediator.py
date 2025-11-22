from fastapi import Depends

from libs.mediator.mediator import Mediator
from libs.mediator.middleware import LoggingMediatorMiddleware
from libs.mediator.registry import BaseCommandRegistry, BaseEventRegistry
from src.container.base import init_container
from src.modules.base.domain.registries import command_registry as base_command_registry
from src.modules.base.domain.registries import event_registry as base_event_registry


def mediator_factory() -> Mediator:
    container = init_container()

    command_registry = BaseCommandRegistry()
    command_registry.merge(base_command_registry)

    event_registry = BaseEventRegistry()
    event_registry.merge(base_event_registry)

    return Mediator(
        command_registry=command_registry,
        event_registry=event_registry,
        container=container,
        middlewares=[LoggingMediatorMiddleware()],
    )


def get_mediator():
    return Depends(mediator_factory)
