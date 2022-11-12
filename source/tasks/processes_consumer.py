import asyncio
import os
import sys
import django
from PIL import Image
from dotenv import load_dotenv
from django.core.mail import send_mail
sys.path.append("/app/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hasker.settings")
django.setup()


load_dotenv()


def email(body):
    message, subject, email = body.split("~!")
    email_from = os.getenv('EMAIL_HOST_USER')
    recipient_list = [email, "disugiske@yandex.ru"]
    send_mail(subject, message, email_from, recipient_list)


# async def update_img(body):
#     user = Profile.objects.filter(id=body)
#     img = Image.open(user.image_url)
#     if img.height > 300 or img.width > 300:
#         output_size = (300, 300)
#         img.thumbnail(output_size)
#         img.save(user.image.path)

