from abc import abstractmethod
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class ISessionable:
    @abstractmethod
    def get_session(self) -> AsyncSession | None:
        pass


class Database(ISessionable):
    def __init__(self, dns, pool_size: int = 5):
        self._engine = create_async_engine(
            dns,
            pool_size=pool_size,
            pool_pre_ping=True,
        )
        self._Session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            expire_on_commit=True,
            bind=self._engine,
        )
        self._session_context: ContextVar[AsyncSession | None] = ContextVar(
            "session_context",
            default=None,
        )

    def start_session(self) -> AsyncSession:
        if not self._session_context.get():
            self._session_context.set(self._Session())
        return self._session_context.get()

    def get_session(self) -> AsyncSession | None:
        return self._session_context.get()


class DBService:
    def __init__(self, database: ISessionable) -> None:
        self.database = database

    @property
    def db_session(self) -> AsyncSession:
        return self.database.get_session()
