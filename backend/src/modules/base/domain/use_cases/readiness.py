from dataclasses import dataclass

from libs.mediator.base import BaseCommand, BaseUseCase, Result
from src.modules.base.domain.entities import CheckStatusItem
from src.modules.base.domain.services.readiness import IReadinessService
from src.modules.base.domain.services.transaction_context import ITransactionContext


class CheckReadinessCommand(BaseCommand):
    pass


class CheckReadinessResult:
    pass


@dataclass
class CheckReadinessUseCase(BaseUseCase[CheckReadinessCommand, list[CheckStatusItem]]):
    transaction_context: ITransactionContext
    readiness_service: IReadinessService

    async def execute(self, command: CheckReadinessCommand) -> Result[list[CheckStatusItem]]:
        async with self.transaction_context:
            result = await self.readiness_service.is_ready()
            return Result(result=result)
