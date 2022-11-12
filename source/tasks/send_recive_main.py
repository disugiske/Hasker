
import os

from aio_pika import DeliveryMode, Message, connect


async def sender(body, queue_name, app_id):
    connection = await connect(f"amqp://guest:guest@{os.getenv('RABBIT_MQ_HOST')}/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        message = Message(
            body,
            delivery_mode=DeliveryMode.PERSISTENT,
            app_id=app_id,
        )
        exchange = await channel.declare_exchange(queue_name, durable=True)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, durable=True)

        # Binding queue
        await queue.bind(exchange, queue_name)

        # Sending the message
        await exchange.publish(
            message,
            routing_key=queue_name,
        )
