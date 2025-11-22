from collections.abc import Callable
from functools import lru_cache
from typing import Any, TypeVar

import punq

from src.config import settings
from src.modules.base.domain.services.readiness import IReadinessService
from src.modules.base.domain.services.transaction_context import ITransactionContext
from src.modules.base.domain.use_cases.readiness import CheckReadinessUseCase
from src.modules.base.gateways.postgresql.database import Database, ISessionable
from src.modules.base.services.readiness import ComposeReadinessService, PostgresqlReadinessService
from src.modules.base.services.transaction_context import DBTransactionContext

T = TypeVar("T")


# TODO расставить типы
class Container(punq.Container):
    def register(
        self,
        service: Any,
        factory=punq.empty,
        instance=punq.empty,
        scope=punq.Scope.transient,
        **kwargs,
    ):
        return super().register(service, factory, instance, scope, **kwargs)

    def resolve(self, service_key: type[T], **kwargs) -> T:
        return super().resolve(service_key, **kwargs)


def _init_container() -> Container:
    container = Container()
    container.register(ISessionable, Database, dns=settings.POSTGRES_DB_URL, scope=punq.Scope.singleton)
    container.register(ITransactionContext, DBTransactionContext)

    container.register(PostgresqlReadinessService)

    def readiness_service_factory():
        return ComposeReadinessService(
            services=[
                container.resolve(PostgresqlReadinessService),
            ]
        )

    container.register(IReadinessService, factory=readiness_service_factory)

    container.register(CheckReadinessUseCase)
    return container


init_container: Callable[[], Container] = lru_cache(1)(_init_container)
