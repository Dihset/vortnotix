from abc import ABC, abstractmethod
from types import TracebackType


class ITransactionContext(ABC):
    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ):
        pass

    @abstractmethod
    async def rollback(self):
        pass
