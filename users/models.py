from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


def profile_image_to_thumbnail(sender, instance, created, **kwargs):
    post_save.disconnect(profile_image_to_thumbnail, sender=Profile)
    if instance.image:
        img = Image.open(instance.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(instance.image.path)

    post_save.connect(profile_image_to_thumbnail, sender=Profile)


post_save.connect(profile_image_to_thumbnail, sender=Profile)
