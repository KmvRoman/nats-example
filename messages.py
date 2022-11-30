import asyncio
from nats_service import ns


async def main():
    await ns.publish_message(subject="user", payload="delayed message",
                             delay="2022-12-1 04:46:10.0")


if __name__ == "__main__":
    asyncio.run(main())