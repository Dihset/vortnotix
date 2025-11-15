import logging
from collections.abc import Iterable
from urllib.request import BaseHandler

from libs.mediator.base import BaseCommand, BaseEvent, BaseUseCase, Result

logger = logging.getLogger(__name__)


class BaseMediatorMiddleware:
    async def pre_run_use_case(self, command: BaseCommand, use_case: BaseUseCase):
        pass

    async def post_run_use_case(self, command: BaseCommand, use_case: BaseUseCase, result: Result):
        pass

    async def pre_run_handler(self, event: BaseEvent, handler: BaseHandler):
        pass

    async def post_run_handler(self, event: BaseEvent, handler: BaseHandler, result_events: Iterable[BaseEvent]):
        pass


class LoggingMediatorMiddleware(BaseMediatorMiddleware):
    async def pre_run_use_case(self, command: BaseCommand, use_case: BaseUseCase):
        logger.info(f"UseCase runned: {use_case=}, {command=}")

    async def post_run_use_case(self, command: BaseCommand, use_case: BaseUseCase, result: Result):
        logger.info(f"UseCase complited: {use_case=}, {command=}, {result=}")

    async def pre_run_handler(self, event: BaseEvent, handler: BaseHandler):
        logger.info(f"Handler runned: {handler=}, {event=}")

    async def post_run_handler(self, event: BaseEvent, handler: BaseHandler, result_events: Iterable[BaseEvent]):
        logger.info(f"Handler complited: {handler=}, {event=}, {result_events=}")
