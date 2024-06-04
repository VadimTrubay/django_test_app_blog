from rest_framework import serializers
from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):
    """ Serializer for the User model. """
    class Meta:
        model = CustomUser
        fields = ('avatar', )
