
from tasks.send_recive_main import sender


async def send_email(message, subject, email):
    body = f"{message}~!{subject}~!{email}".encode()
    queue_name = "email"
    await sender(body, queue_name, 1)

async def send_img(user_id):
    body = str(user_id).encode()
    queue_name = "img"
    await sender(body, queue_name, 2)

