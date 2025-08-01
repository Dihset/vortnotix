from pydantic import BaseModel


class ReceiverSchema(BaseModel):
    channel_type: str  # TODO make Enum
    address: dict[str, str]


# class ContentSchema(BaseModel):
#     pass


class SendMessageSchema(BaseModel):
    receiver: ReceiverSchema
    content: dict[str, str]
