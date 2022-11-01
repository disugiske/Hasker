import asyncio
from aio_pika import DeliveryMode, Message, connect

user, post_id = "admin", '23'


async def send_email(message,subject, email):
    body = f'{message}~!{subject}~!{email}'.encode()
    queue_name = 'email'
    connection = await connect("amqp://guest:guest@localhost/")

    async with connection:
        # Creating a channel
        channel = await connection.channel()
        message = Message(
            body,
            delivery_mode=DeliveryMode.PERSISTENT,
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
