from pydantic import BaseModel


class ApiSchema[DataT: BaseModel](BaseModel):
    data: DataT | None
    error: None = None
