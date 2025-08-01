from fastapi import APIRouter

from src.api.v1.send.schemas import SendMessageSchema

async_router = APIRouter(prefix="/async")


@async_router.post("/send")
async def asycn_send_message(payload: SendMessageSchema):
    return {"data": {"task_id": 123}}


sync_router = APIRouter(prefix="/sync")


@sync_router.post("/send")
async def sync_send_message(payload: SendMessageSchema):
    return {"data": {"status": "sended"}}
