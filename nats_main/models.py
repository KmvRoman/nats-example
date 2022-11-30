from pydantic import BaseModel, validator
from nats.js import JetStreamContext
from nats.aio.client import Client


class Connect(BaseModel):
    ns: Client
    js: JetStreamContext

    class Config:
        arbitrary_types_allowed = True

    @validator("ns")
    def check_ns(cls, value: Client):
        if isinstance(value, Client):
            return value
        raise ValueError("value ns must be instance of nats.aio.client.Client")

    @validator("js")
    def check_js(cls, value):
        if isinstance(value, JetStreamContext):
            return value
        raise ValueError("value js must be instance of nats.js.JetStreamContext")