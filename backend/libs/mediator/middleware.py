import logging
from collections.abc import Awaitable, Callable, Sequence
from typing import TypeVar

from libs.mediator.base import BaseCommand, BaseEvent, BaseHandler, BaseUseCase, EventStore, Result

logger = logging.getLogger(__name__)

R = TypeVar("R")


class BaseMediatorMiddleware:
    async def wrap_use_case(
        self,
        command: BaseCommand,
        use_case: BaseUseCase,
        call_next: Callable[[BaseCommand, BaseUseCase], Awaitable[Result[R]]],
    ) -> Result[R]:
        return await call_next(command, use_case)

    async def wrap_handler(
        self,
        event: BaseEvent,
        handler: BaseHandler,
        call_next: Callable[[BaseEvent, BaseHandler], Awaitable[EventStore | None]],
    ) -> EventStore | None:
        return await call_next(event, handler)


def compose_use_case(
    middlewares: Sequence[BaseMediatorMiddleware],
) -> Callable[[BaseCommand, BaseUseCase], Awaitable[Result[R]]]:
    def wrap(index: int):
        if index == len(middlewares):

            async def execute(command: BaseCommand, use_case: BaseUseCase) -> Result[R]:
                return await use_case.execute(command)

            return execute

        async def current(command: BaseCommand, use_case: BaseUseCase) -> Result[R]:
            return await middlewares[index].wrap_use_case(command, use_case, wrap(index + 1))

        return current

    return wrap(0)


def compose_handler(
    middlewares: Sequence[BaseMediatorMiddleware],
):
    def wrap(index: int):
        if index == len(middlewares):

            async def execute(event: BaseEvent, handler: BaseHandler) -> EventStore | None:
                return await handler.execute(event)

            return execute

        async def current(event: BaseEvent, handler: BaseHandler) -> EventStore | None:
            return await middlewares[index].wrap_handler(event, handler, wrap(index + 1))

        return current

    return wrap(0)


class LoggingMediatorMiddleware(BaseMediatorMiddleware):
    async def wrap_use_case(
        self,
        command: BaseCommand,
        use_case: BaseUseCase,
        call_next: Callable[[BaseCommand, BaseUseCase], Awaitable[Result[R]]],
    ) -> Result[R]:
        logger.info(f"UseCase runned: {use_case=}, {command=}")
        result = await call_next(command, use_case)
        logger.info(f"UseCase complited: {use_case=}, {command=}, {result=}")
        return result

    async def wrap_handler(
        self,
        event: BaseEvent,
        handler: BaseHandler,
        call_next: Callable[[BaseEvent, BaseHandler], Awaitable[EventStore | None]],
    ) -> EventStore | None:
        logger.info(f"Handler runned: {handler=}, {event=}")
        result_events = await call_next(event, handler)
        logger.info(f"Handler complited: {handler=}, {event=}, {result_events=}")
        return result_events
