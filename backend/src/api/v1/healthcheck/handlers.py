from fastapi import APIRouter

from libs.mediator.mediator import Mediator
from src.api.v1.base.schemas import ApiSchema
from src.api.v1.healthcheck.schemas import HealthCheckResult, ReadinessCheckResult
from src.container.mediator import get_mediator
from src.modules.base.domain.use_cases.readiness import CheckReadinessCommand

router = APIRouter()


@router.get(
    "/healthcheck",
    response_model=ApiSchema[HealthCheckResult],
)
async def get_healthcheck() -> ApiSchema[HealthCheckResult]:
    return ApiSchema(data=HealthCheckResult())


@router.get(
    "/readiness",
    response_model=ApiSchema[ReadinessCheckResult],
)
async def get_readiness(mediator: Mediator = get_mediator()) -> ApiSchema[ReadinessCheckResult]:
    result = await mediator.handle(CheckReadinessCommand())
    return ApiSchema(data=ReadinessCheckResult.from_entity(result))
