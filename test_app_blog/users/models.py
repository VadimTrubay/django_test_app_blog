from django.db import models
from django.contrib.auth.models import AbstractUser


def get_path_name(instance, filename):
    path = 'media/avatar/'
    name = instance.user.id + "-" + instance.user.email
    path = path + name
    return path


# custom User model
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=get_path_name, blank=True, null=True)

    def __str__(self):
        return self.avatar
