import asyncio
import os

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from django.core.mail import send_mail

from hasker import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hasker.settings')


async def main_time(message):
    body = message.body.decode()
    message, subject, email = body.split('~!')
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, 'disugiske@yandex.ru']
    send_mail(subject, message, email_from, recipient_list)


async def process_message(message: AbstractIncomingMessage, ) -> None:
    async with message.process():
        await main_time(message)


async def main() -> None:
    connection = await connect(f"amqp://guest:guest@{os.getenv('RABBIT_MQ_HOST')}/")

    queue_name = "email"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name,
                                        durable=True
                                        )

    await queue.consume(process_message)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
