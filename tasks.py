from datetime import datetime
from nats_main.client import Nats
from nats.aio.msg import Msg


async def qsub_a(message: Msg):
    if await Nats.check_delay(delay=message.headers.get("delay", "2000-01-01 00:00:00.0"),
                              datetime_now=datetime.now().timestamp()):
        print("HANDLER A", message.headers)
        await message.ack()
    else:
        print("nak A")
        await message.nak(await Nats.delay_in_str(delay=message.headers.get("delay", "2000-01-01 00:00:00.0"),
                                                  datetime_now=datetime.now().timestamp()))


async def qsub_b(message: Msg):
    if await Nats.check_delay(delay=message.headers.get("delay", "2000-01-01 00:00:00.0"),
                              datetime_now=datetime.now().timestamp()):
        print("HANDLER B", message.headers)
        await message.ack()
    else:
        print("nak B")
        await message.nak(await Nats.delay_in_str(delay=message.headers.get("delay", "2000-01-01 00:00:00.0"),
                                                  datetime_now=datetime.now().timestamp()))
