from libs.mediator.registry import BaseCommandRegistry, BaseEventRegistry
from src.modules.base.domain.use_cases.readiness import CheckReadinessCommand, CheckReadinessUseCase

command_registry = BaseCommandRegistry()
command_registry.register(CheckReadinessCommand, CheckReadinessUseCase)

event_registry = BaseEventRegistry()
