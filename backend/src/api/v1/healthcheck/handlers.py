from fastapi import APIRouter

from src.api.v1.base.schemas import ApiSchema
from src.api.v1.healthcheck.schemas import HealthCheckResult

router = APIRouter()


@router.get(
    "/healthcheck",
    response_model=ApiSchema[HealthCheckResult],
)
async def get_healthcheck() -> ApiSchema[HealthCheckResult]:
    return ApiSchema(data=HealthCheckResult())
