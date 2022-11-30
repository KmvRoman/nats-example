import asyncio
from tasks import qsub_a, qsub_b
from nats_main import Nats, Connect
from config.parse_conf import parse_config
from config.config import BASE_DIR


class NatsService(Nats):
    async def setup_subs(self, connection: Connect) -> None:
        await connection.js.subscribe(subject="user", queue="match_bot", cb=qsub_a)
        await connection.js.subscribe(subject="user", queue="match_bot", cb=qsub_b)

    async def actions(self, connection: Connect) -> None:
        pass


config = parse_config(BASE_DIR / "natspy" / "config" / "config.yaml")

ns = NatsService(
    user=config.nats.user,
    password=config.nats.password,
    ip_address=config.nats.ip_address,
    port=config.nats.nats_port,
)


if __name__ == "__main__":
    try:
        asyncio.run(ns.start_polling())
    except KeyboardInterrupt:
        print("stop")
    finally:
        asyncio.run(ns.stop_polling())