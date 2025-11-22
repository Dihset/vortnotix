from dataclasses import dataclass
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.base.domain.services.transaction_context import ITransactionContext
from src.modules.base.gateways.postgresql.database import ISessionable


@dataclass
class DBTransactionContext(ITransactionContext):
    database: ISessionable

    async def __aenter__(self):
        self._session: AsyncSession = self.database.start_session()

    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ):
        if not exc_value:
            await self._session.commit()
        else:
            await self._session.rollback()

        await self._session.close()

    async def rollback(self):
        self._session.rollback()
