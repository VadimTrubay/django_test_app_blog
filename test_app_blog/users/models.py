from django.db import models
from django.contrib.auth.models import AbstractUser


def get_path_name(instance, filename):
    
    """
    The get_path_name function takes in an instance of the UserProfile model and a filename.
    It then creates a path variable that is equal to 'media/avatar/' + the user's id + &quot;-&quot; + their email address.
    This ensures that each user has their own unique avatar image file name.
    
    :param instance: Get the user id and email
    :param filename: Get the name of the file that is being uploaded
    :return: The path for the image
    :doc-author: Trelent
    """
    path = 'media/avatar/'
    name = instance.user.id + "-" + instance.user.email
    path = path + name
    return path



class CustomUser(AbstractUser):
    """ This class inherits from the AbstractUser class. """
    avatar = models.ImageField(upload_to=get_path_name, blank=True, null=True)

    def __str__(self):
        return self.avatar
