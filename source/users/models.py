from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

from hasker import settings


class Profile(AbstractUser):
    image = models.ImageField(upload_to="profile_pics",
                              default="default/default.jpg")

    def __str__(self):
        return self.username

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return f'{settings.MEDIA_URL}default/default.jpg'

    def save(self, *args, **kwargs):
        super().save()
        if kwargs.get('update_fields') is None:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)