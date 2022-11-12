import asyncio
import os

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from processes_consumer import email


async def process_message(message):
    async with message.process():
        body: AbstractIncomingMessage = message.body.decode()
        if int(message.app_id) == 1:
            email(body)


async def main(queue_name) -> None:
    connection = await connect(f"amqp://guest:guest@{os.getenv('RABBIT_MQ_HOST')}/")


    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main("email"))
