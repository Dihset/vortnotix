import logging
from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy.sql import text

from src.modules.base.domain.entities import CheckStatus, CheckStatusItem
from src.modules.base.domain.services.readiness import IReadinessService
from src.modules.base.gateways.postgresql.database import DBService


class PostgresqlReadinessService(IReadinessService, DBService):
    async def is_ready(self) -> list[CheckStatusItem]:
        try:
            await self.db_session.execute(text("select 1"))
            return [CheckStatusItem(service="postgresql", status=CheckStatus.ok)]
        except Exception as e:
            logging.exception(f"Error: {e}")
            return [CheckStatusItem(service="postgresql", status=CheckStatus.error)]


@dataclass
class ComposeReadinessService(IReadinessService):
    services: Sequence[IReadinessService]

    async def is_ready(self) -> list[CheckStatusItem]:
        result: Sequence[CheckStatusItem] = []
        for service in self.services:
            result.extend(await service.is_ready())
        return result
