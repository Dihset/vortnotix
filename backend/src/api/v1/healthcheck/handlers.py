from fastapi import APIRouter

from src.api.v1.base.schemas import ApiSchema
from src.api.v1.healthcheck.schemas import HealthCheckResult, ReadinessCheckResult
from src.container.base import init_container
from src.modules.base.domain.use_cases.readiness import CheckReadinessCommand, CheckReadinessUseCase

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
async def get_readiness() -> ApiSchema[ReadinessCheckResult]:
    container = init_container()
    use_case = container.resolve(CheckReadinessUseCase)
    result = await use_case.execute(CheckReadinessCommand())
    return ApiSchema(data=ReadinessCheckResult.from_entity(result.result))
