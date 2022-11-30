from nats import connect
import asyncio
from nats.js import JetStreamContext
from nats_main.models import Connect
import dateutil.parser
from datetime import datetime


class Nats:
    def __init__(
            self,
            user: str,
            password: str,
            ip_address: str,
            port: int
    ):
        self._user = user
        self._password = password
        self._ip_address = ip_address
        self._port = port

    async def _connect_service(self) -> Connect:
        self.__client = await connect(f"nats://{self._user}:{self._password}@{self._ip_address}:{self._port}")
        self.__stream = self.__client.jetstream()
        return Connect(ns=self.__client, js=self.__stream)

    async def get_streams_info(self) -> JetStreamContext.streams_info:
        conn: Connect = await self._connect_service()
        return await conn.js.streams_info()

    async def start_polling(self, timeout: int = 20) -> None:
        conn: Connect = await self._connect_service()
        await self.actions(connection=conn)
        while True:
            await self.setup_subs(connection=conn)
            await asyncio.sleep(timeout)

    async def stop_polling(self) -> None:
        conn: Connect = await self._connect_service()
        await conn.ns.close()

    async def setup_subs(self, connection: Connect) -> None:
        pass

    async def actions(self, connection: Connect) -> None:
        pass

    async def publish_message(
            self,
            subject: str,
            payload: str,
            timeout: float = None,
            stream: str = None,
            **headers
    ):
        conn: Connect = await self._connect_service()
        return await conn.js.publish(
            subject=subject,
            stream=stream,
            payload=payload.encode(),
            timeout=timeout,
            headers={
                **headers,
            }
        )

    async def delete_message(self, stream: str, seq: int):
        conn: Connect = await self._connect_service()
        await conn.js.delete_msg(stream_name=stream, seq=seq)

    @staticmethod
    async def delay_in_str(delay: str, datetime_now: datetime.timestamp) -> datetime.timestamp:
        return dateutil.parser.parse(delay).timestamp() - datetime_now

    @staticmethod
    async def check_delay(delay: str, datetime_now: datetime.timestamp) -> bool:
        return (dateutil.parser.parse(delay).timestamp() - datetime_now) <= 0
